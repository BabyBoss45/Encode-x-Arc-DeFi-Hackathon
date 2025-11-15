#!/bin/bash
# Скрипт для запуска backend

echo "🚀 Запуск BossBoard Backend..."

cd backend

# Проверяем наличие .env файла
if [ ! -f .env ]; then
    echo "📝 Создаю .env файл..."
    cat > .env << 'EOF'
DATABASE_URL=sqlite:///./bossboard.db
JWT_SECRET_KEY=my-secret-key-change-in-production
CIRCLE_API_KEY=test-key
CIRCLE_BASE_URL=https://api.circle.com/v1
EOF
    echo "✅ .env файл создан"
fi

# Проверяем зависимости
echo "📦 Проверяю зависимости..."
pip3 install -q -r requirements.txt

# Запускаем backend
echo "🚀 Запуск на http://localhost:8000"
python3 main.py

