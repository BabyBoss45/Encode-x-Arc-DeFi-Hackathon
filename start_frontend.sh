#!/bin/bash
# Скрипт для запуска frontend

echo "🚀 Запуск BossBoard Frontend..."

cd src

# Проверяем зависимости
echo "📦 Проверяю зависимости..."
pip3 install -q fastapi uvicorn jinja2 python-multipart requests

# Запускаем frontend
echo "🚀 Запуск на http://localhost:8001"
python3 frontend.py

