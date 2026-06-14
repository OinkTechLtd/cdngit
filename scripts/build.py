#!/usr/bin/env python3
"""
Генератор статического сайта из schedule.json
"""
import json, shutil
from pathlib import Path
from datetime import datetime, timezone, timedelta

MSK = timezone(timedelta(hours=3))
Path("docs").mkdir(exist_ok=True)

# Копируем index.html в docs/
src = Path("index.html")
dst = Path("docs/index.html")

if src.exists():
    # Если есть данные - вшиваем их в HTML
    try:
        data = json.loads(Path("data/schedule.json").read_text("utf-8"))
        html = src.read_text("utf-8")
        # Вставляем данные как JS переменная
        inject = f"<script>window.__EPG_DATA__={json.dumps(data, ensure_ascii=False)};</script>"
        html = html.replace("</head>", inject + "\n</head>", 1)
        dst.write_text(html, "utf-8")
        print(f"✅ docs/index.html с данными EPG")
    except Exception as e:
        shutil.copy(src, dst)
        print(f"ℹ️  docs/index.html (без данных: {e})")
else:
    print("⚠️  index.html не найден")

# Копируем data/ в docs/data/
data_dst = Path("docs/data")
data_dst.mkdir(exist_ok=True)
for f in Path("data").glob("*.json"):
    shutil.copy(f, data_dst / f.name)
for f in Path("data").glob("*.xml"):
    shutil.copy(f, data_dst / f.name)

print("✅ Статический сайт собран в docs/")
