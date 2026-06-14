#!/usr/bin/env python3
"""
live-programm | EPG Search Robot
Поисковой робот расписания ТВ-программ
OinkTech Ltd | FUN RUSSIA CRMP
"""

import asyncio
import aiohttp
import json
import os
import re
import sys
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import quote_plus, urlencode
import xml.etree.ElementTree as ET

# ── Настройка логов ────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('data/robot.log', encoding='utf-8'),
    ]
)
log = logging.getLogger('epg-robot')

MSK = timezone(timedelta(hours=3))

# ── Каналы которые мы ищем ────────────────────────────────────
CHANNELS = [
    {"id": "perviy",     "name": "Первый канал",    "site_id": "1tv",        "group": "Федеральные"},
    {"id": "rossiya1",   "name": "Россия 1",         "site_id": "russia1",    "group": "Федеральные"},
    {"id": "ntv",        "name": "НТВ",              "site_id": "ntv",        "group": "Федеральные"},
    {"id": "ctc",        "name": "СТС",              "site_id": "ctc",        "group": "Федеральные"},
    {"id": "ren",        "name": "РЕН ТВ",           "site_id": "rentv",      "group": "Федеральные"},
    {"id": "tnt",        "name": "ТНТ",              "site_id": "tnt",        "group": "Федеральные"},
    {"id": "5tv",        "name": "Пятый канал",      "site_id": "5tv",        "group": "Федеральные"},
    {"id": "muz",        "name": "МУЗ-ТВ",           "site_id": "muztv",      "group": "Музыка"},
    {"id": "zvez",       "name": "Звезда",           "site_id": "zvezda",     "group": "Федеральные"},
    {"id": "match",      "name": "Матч! ТВ",         "site_id": "matchtv",    "group": "Спорт"},
    {"id": "russia24",   "name": "Россия 24",        "site_id": "russia24",   "group": "Новости"},
    {"id": "o_tv",       "name": "ОТР",              "site_id": "otr",        "group": "Федеральные"},
    {"id": "dom_kino",   "name": "Дом Кино",         "site_id": "domkino",    "group": "Кино"},
    {"id": "nauka",      "name": "Наука",            "site_id": "nauka",      "group": "Познание"},
    {"id": "karusel",    "name": "Карусель",         "site_id": "karusel",    "group": "Детские"},
    {"id": "tvc",        "name": "ТВ Центр",         "site_id": "tvc",        "group": "Федеральные"},
    {"id": "tb3",        "name": "ТВ-3",             "site_id": "tv3",        "group": "Развлечения"},
    {"id": "sas",        "name": "Суббота!",         "site_id": "subbota",    "group": "Развлечения"},
    {"id": "chetv",      "name": "Четвёрка",         "site_id": "chetvertiy", "group": "Развлечения"},
    {"id": "dozhd",      "name": "Дождь",            "site_id": "tvrain",     "group": "Новости"},
]

# ── Источники EPG ─────────────────────────────────────────────
EPG_SOURCES = [
    # XMLTV от epg.one — российское EPG
    "https://epg.one/epg.xml.gz",
    "https://epg.one/epg.xml",
    # Другие публичные EPG
    "https://www.epg.one/epg/Russia.xml",
    "https://raw.githubusercontent.com/dp247/Freeview-EPG/master/epg.xml",
]

# Сайты с расписанием для парсинга
SCHEDULE_SITES = [
    {
        "name": "tv.mail.ru",
        "url":  "https://tv.mail.ru/ajax/channel/?channel_id={site_id}&region_id=8&date={date}",
        "type": "mail",
    },
    {
        "name": "programma.tv",
        "url":  "https://programma.tv/tvprogramm/{site_id}/{date}/",
        "type": "programma",
    },
    {
        "name": "vsetv.com",
        "url":  "https://www.vsetv.com/schedule_{site_id}_{date}.html",
        "type": "vsetv",
    },
    {
        "name": "1tv.ru_api",
        "url":  "https://www.1tv.ru/api/schedule?date={date}",
        "type": "1tv",
        "only_id": "perviy",
    },
    {
        "name": "ctc_api",
        "url":  "https://api.ctc.ru/api/schedule?date={date}",
        "type": "ctc",
        "only_id": "ctc",
    },
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,application/json,*/*;q=0.8",
}


# ═══════════════════════════════════════════════════════════════
class EPGRobot:
    def __init__(self):
        self.data = {}       # { channel_id: [programme, ...] }
        self.session = None
        Path("data").mkdir(exist_ok=True)

    # ── Главный запуск ────────────────────────────────────────
    async def run(self):
        log.info("🤖 Запуск поискового робота EPG...")
        async with aiohttp.ClientSession(headers=HEADERS, timeout=aiohttp.ClientTimeout(total=30)) as sess:
            self.session = sess

            tasks = []
            # Параллельно ищем расписание для каждого канала
            for ch in CHANNELS:
                tasks.append(self.fetch_channel(ch))

            results = await asyncio.gather(*tasks, return_exceptions=True)

            for ch, res in zip(CHANNELS, results):
                if isinstance(res, Exception):
                    log.warning(f"⚠️  {ch['name']}: {res}")
                elif res:
                    self.data[ch["id"]] = res
                    log.info(f"✅ {ch['name']}: {len(res)} передач")

        total = sum(len(v) for v in self.data.values())
        log.info(f"📺 Итого: {total} передач по {len(self.data)} каналам")
        self.save()

    # ── Получить расписание одного канала ─────────────────────
    async def fetch_channel(self, ch):
        now = datetime.now(MSK)
        today = now.strftime("%Y-%m-%d")
        tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")

        programmes = []

        # Пробуем все источники по очереди
        for src in SCHEDULE_SITES:
            if src.get("only_id") and src["only_id"] != ch["id"]:
                continue
            try:
                progs = await self.try_source(src, ch, today)
                if progs:
                    programmes.extend(progs)
                    break  # нашли — не ищем дальше
            except Exception as e:
                log.debug(f"  {src['name']} → {ch['name']}: {e}")

        # Если ничего не нашли — используем fallback Google/Яндекс поиск
        if not programmes:
            programmes = await self.search_fallback(ch, today)

        return programmes or self.generate_placeholder(ch, now)

    # ── Попытка получить с конкретного источника ──────────────
    async def try_source(self, src, ch, date):
        url = src["url"].format(
            site_id=ch["site_id"],
            date=date,
            channel_id=ch["site_id"],
        )
        async with self.session.get(url) as r:
            if r.status != 200:
                return None
            ct = r.headers.get("Content-Type", "")
            if "json" in ct:
                data = await r.json(content_type=None)
            else:
                data = await r.text()

        parser = getattr(self, f"parse_{src['type']}", None)
        if parser:
            return parser(data, ch)
        return None

    # ── Парсеры ───────────────────────────────────────────────

    def parse_mail(self, data, ch):
        """tv.mail.ru JSON"""
        progs = []
        items = []
        if isinstance(data, dict):
            items = data.get("rows", data.get("schedule", []))
        elif isinstance(data, list):
            items = data
        for item in items:
            try:
                title = item.get("title") or item.get("name", "")
                start = item.get("start_ut") or item.get("start_time")
                end   = item.get("end_ut")   or item.get("end_time")
                desc  = item.get("description", "")
                genre = item.get("genre", "")
                if not title: continue
                progs.append(self._prog(ch, title, start, end, desc, genre))
            except Exception:
                pass
        return progs

    def parse_programma(self, html, ch):
        """programma.tv HTML"""
        progs = []
        # Ищем паттерны <span class="start-time">21:00</span> ... <span class="program-name">Название</span>
        pattern = r'(\d{1,2}:\d{2})\s*</[^>]+>\s*(?:<[^>]+>)*\s*([^<]{3,80})'
        now = datetime.now(MSK)
        for m in re.finditer(pattern, html):
            t, name = m.group(1).strip(), m.group(2).strip()
            name = re.sub(r'\s+', ' ', name)
            if len(name) < 3 or len(name) > 100: continue
            h, mi = map(int, t.split(':'))
            dt = now.replace(hour=h, minute=mi, second=0, microsecond=0)
            progs.append(self._prog(ch, name, dt.timestamp(), None))
        return progs

    def parse_vsetv(self, html, ch):
        """vsetv.com HTML"""
        return self.parse_programma(html, ch)

    def parse_1tv(self, data, ch):
        """1tv.ru JSON API"""
        progs = []
        events = []
        if isinstance(data, dict):
            events = data.get("schedule", data.get("events", []))
        for e in events:
            title = e.get("title") or e.get("name", "")
            if not title: continue
            start = e.get("start") or e.get("time_start")
            end   = e.get("end")   or e.get("time_end")
            desc  = e.get("description", "")
            progs.append(self._prog(ch, title, start, end, desc))
        return progs

    def parse_ctc(self, data, ch):
        """CTC API JSON"""
        return self.parse_1tv(data, ch)

    # ── Fallback: поиск расписания через публичный API ────────
    async def search_fallback(self, ch, date):
        """
        Запасной вариант: запрашиваем epg.best / epg.ottplay и т.д.
        """
        try:
            # epg.best — публичный JSON EPG
            url = f"https://epg.best/ch/{ch['site_id']}/{date}.json"
            async with self.session.get(url) as r:
                if r.status == 200:
                    data = await r.json(content_type=None)
                    progs = []
                    for item in (data if isinstance(data, list) else data.get("schedule", [])):
                        title = item.get("title") or item.get("name", "")
                        if not title: continue
                        progs.append(self._prog(
                            ch, title,
                            item.get("start") or item.get("time"),
                            item.get("stop")  or item.get("end"),
                            item.get("desc", ""),
                        ))
                    if progs:
                        return progs
        except Exception:
            pass

        try:
            # ottplay EPG
            url = f"https://epg.ottplay.com/epg/{ch['site_id']}.json"
            async with self.session.get(url) as r:
                if r.status == 200:
                    data = await r.json(content_type=None)
                    progs = []
                    for item in (data if isinstance(data, list) else []):
                        title = item.get("title", "")
                        if not title: continue
                        progs.append(self._prog(ch, title, item.get("start"), item.get("stop")))
                    if progs:
                        return progs
        except Exception:
            pass

        return []

    # ── Заглушка если ничего не найдено ──────────────────────
    def generate_placeholder(self, ch, now):
        """Генерируем базовую сетку вещания"""
        slots = [
            (6, 0, "Утреннее вещание"),
            (9, 0, "Дневное вещание"),
            (13, 0, "Обеденный выпуск"),
            (15, 0, "Послеполуденные программы"),
            (18, 0, "Вечерние новости"),
            (19, 0, "Прайм-тайм"),
            (21, 30, "Ночное вещание"),
        ]
        progs = []
        for i, (h, m, title) in enumerate(slots):
            dt = now.replace(hour=h, minute=m, second=0, microsecond=0)
            next_h, next_m, _ = slots[i+1] if i+1 < len(slots) else (23, 59, "")
            end_dt = now.replace(hour=next_h, minute=next_m, second=0, microsecond=0)
            progs.append(self._prog(ch, title, dt.timestamp(), end_dt.timestamp()))
        return progs

    # ── Конструктор программы ─────────────────────────────────
    def _prog(self, ch, title, start=None, stop=None, desc="", genre=""):
        now = datetime.now(MSK)

        def to_ts(v):
            if v is None: return None
            if isinstance(v, (int, float)): return float(v)
            if isinstance(v, str):
                for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%H:%M"):
                    try:
                        dt = datetime.strptime(v[:len(fmt)], fmt)
                        if dt.year == 1900:
                            dt = dt.replace(year=now.year, month=now.month, day=now.day)
                        return dt.replace(tzinfo=MSK).timestamp()
                    except ValueError:
                        pass
            return None

        start_ts = to_ts(start) or now.timestamp()
        stop_ts  = to_ts(stop)  or (start_ts + 3600)

        return {
            "channel":  ch["id"],
            "title":    title,
            "start":    int(start_ts),
            "stop":     int(stop_ts),
            "desc":     desc or "",
            "genre":    genre or "",
            "live":     int(start_ts) <= int(now.timestamp()) < int(stop_ts),
        }

    # ── Сохранение ────────────────────────────────────────────
    def save(self):
        now = datetime.now(MSK)
        out = {
            "updated":   now.isoformat(),
            "updated_ts": int(now.timestamp()),
            "channels":  {
                ch["id"]: {
                    "id":    ch["id"],
                    "name":  ch["name"],
                    "group": ch["group"],
                    "site_id": ch["site_id"],
                }
                for ch in CHANNELS
            },
            "schedule": self.data,
        }
        Path("data/schedule.json").write_text(
            json.dumps(out, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
        )
        log.info("💾 data/schedule.json сохранён")

        # Также сохраняем XMLTV формат
        self.save_xmltv(now)

    def save_xmltv(self, now):
        root = ET.Element("tv", {
            "date": now.strftime("%Y%m%d%H%M%S %z"),
            "source-info-name": "live-programm robot",
            "generator-info-name": "OinkTech live-programm",
        })
        for ch in CHANNELS:
            c = ET.SubElement(root, "channel", id=ch["id"])
            ET.SubElement(c, "display-name", lang="ru").text = ch["name"]

        for ch in CHANNELS:
            for prog in self.data.get(ch["id"], []):
                fmt = "%Y%m%d%H%M%S +0300"
                p = ET.SubElement(root, "programme", {
                    "start":   datetime.fromtimestamp(prog["start"], MSK).strftime(fmt),
                    "stop":    datetime.fromtimestamp(prog["stop"],  MSK).strftime(fmt),
                    "channel": ch["id"],
                })
                ET.SubElement(p, "title", lang="ru").text = prog["title"]
                if prog.get("desc"):
                    ET.SubElement(p, "desc", lang="ru").text = prog["desc"]
                if prog.get("genre"):
                    ET.SubElement(p, "category", lang="ru").text = prog["genre"]

        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")
        tree.write("data/epg.xml", encoding="utf-8", xml_declaration=True)
        log.info("📡 data/epg.xml сохранён")


# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    asyncio.run(EPGRobot().run())
