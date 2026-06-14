# 📺 LiveПрограмма

> **Поисковой робот TV-расписания + веб-гид в стиле TikTok**  
> Робот сам ищет расписание каналов в интернете каждые 3 часа. Видишь что идёт сейчас — жмёшь play.

![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-каждые_3ч-blue?logo=github-actions)
![Python](https://img.shields.io/badge/Python-3.11-brightgreen?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Made by](https://img.shields.io/badge/OinkTech_Ltd-FUN_RUSSIA_CRMP-red)

---

## 🔥 Что это

**live-programm** — это автономный проект в стиле TikTok для просмотра TV-программы российских каналов:

- **Поисковой робот** (`scripts/epg_robot.py`) ищет расписание по интернету без баз данных — парсит tv.mail.ru, programma.tv, vsetv.com, официальные API каналов
- **Авто-обновление** через GitHub Actions каждые 3 часа — никакого ручного труда
- **TikTok-интерфейс** — листаешь каналы вертикально, видишь что идёт СЕЙЧАС с прогресс-баром
- **Встроенный плеер** — PlayerJS из [OinkTechLtd/rulive](https://github.com/OinkTechLtd/rulive) + fallback на hls.js
- **Плейлисты** из [OinkTechLLC/livem3u](https://github.com/OinkTechLLC/livem3u) и [OinkTechLtd/rulive](https://github.com/OinkTechLtd/rulive)

---

## 📱 Интерфейс

```
┌────────────────────────────┐
│ 🔴 LiveПрограмма       🔍 │  ← Поиск по программе
├────────────────────────────┤
│ [Все][Первый][Россия][НТВ]│  ← Вкладки каналов
├────────────────────────────┤
│                            │
│  ▶  [кнопка плеера]       │  ← Тап → смотреть в эфире
│                            │
│  🔴 В ЭФИРЕ               │
│  Первый канал              │
│  Вечерние новости          │
│  21:00 — 22:00 · 60 мин   │
│  ████████████░░░░ 75%      │  ← Прогресс передачи
│                            │
│  Далее:                    │
│  22:00  Ночные новости     │
│  23:00  Фильм              │
│                            │
├────────────────────────────┤
│ 📺 Эфир  📋 Каналы  🔍   │  ← Нав-бар TikTok стиль
└────────────────────────────┘
     ↕ Листаешь вверх/вниз
```

---

## 🚀 Деплой на GitHub Pages

### 1. Форкни репо

```bash
git clone https://github.com/YOUR_NAME/live-programm.git
cd live-programm
```

### 2. Включи GitHub Pages

`Settings → Pages → Source → Deploy from branch → main / docs`

### 3. Запусти робота вручную первый раз

`Actions → 🤖 EPG Robot → Run workflow`

### 4. Готово ✅

Сайт будет доступен по адресу:
```
https://YOUR_NAME.github.io/live-programm/
```

---

## 🤖 Как работает поисковой робот

```
epg_robot.py
    │
    ├─ Для каждого канала параллельно:
    │   ├─ tv.mail.ru JSON API
    │   ├─ programma.tv (парсинг HTML)
    │   ├─ vsetv.com (парсинг HTML)
    │   ├─ 1tv.ru API (для Первого)
    │   ├─ ctc.ru API (для СТС)
    │   └─ Fallback: epg.best / epg.ottplay
    │
    ├─ Сохраняет data/schedule.json
    ├─ Генерирует data/epg.xml (XMLTV)
    └─ build.py → docs/index.html (с данными)
```

**Без баз данных.** Каждые 3 часа робот сам находит актуальное расписание по открытым источникам.

---

## 📁 Структура

```
live-programm/
├── .github/
│   └── workflows/
│       └── epg.yml          # Actions: каждые 3 часа
├── scripts/
│   ├── epg_robot.py         # 🤖 Поисковой робот EPG
│   └── build.py             # Генератор статики
├── data/
│   ├── schedule.json        # Расписание (генерируется)
│   └── epg.xml              # XMLTV формат (генерируется)
├── docs/                    # GitHub Pages (генерируется)
├── index.html               # TikTok-гид (главная страница)
├── player.html              # Встроенный плеер
├── requirements.txt
└── README.md
```

---

## 📡 Плейлисты

Используются плейлисты из репозиториев OinkTech:

| Плейлист | Ссылка |
|---|---|
| **Основной** | `https://raw.githubusercontent.com/OinkTechLLC/livem3u/main/zabava-full.m3u` |
| **Smotrim** | `https://raw.githubusercontent.com/OinkTechLLC/livem3u/main/smotrim.m3u` |
| **Резервный** | `https://raw.githubusercontent.com/OinkTechLtd/rulive/main/russ.m3u` |

---

## 📺 Поддерживаемые каналы

| Канал | Группа |
|---|---|
| Первый канал, Россия 1, НТВ, ОТР, ТВ Центр | Федеральные |
| Пятый канал, РЕН ТВ, СТС, ТНТ, ТВ-3, Суббота! | Федеральные |
| Россия 24, Дождь | Новости |
| Матч! ТВ | Спорт |
| МУЗ-ТВ | Музыка |
| Карусель | Детские |
| Наука | Познание |
| Дом Кино | Кино |
| Звезда | Федеральные |

---

## ⚙️ Локальный запуск робота

```bash
pip install aiohttp
python scripts/epg_robot.py
```

Сохраняет `data/schedule.json` и `data/epg.xml`.

---

## 🛠️ GitHub Actions

Воркфлоу `.github/workflows/epg.yml` запускается:
- **Каждые 3 часа** автоматически
- **При пуше** в `main` (если изменились скрипты)
- **Вручную** через `workflow_dispatch`

Каждый запуск:
1. Запускает `epg_robot.py`
2. Запускает `build.py`
3. Коммитит обновлённые файлы в репо

---

## 🌐 Как подключить как EPG к IPTV плееру

XMLTV файл доступен по адресу:
```
https://YOUR_NAME.github.io/live-programm/data/epg.xml
```

Вставляй в TiviMate, OttPlayer, IPTV Smarters и т.д.

---

## 👤 Автор

**OinkTech Ltd** · FUN RUSSIA CRMP

*⭐ Звезда если зашло!*
