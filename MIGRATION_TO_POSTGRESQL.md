# 🚀 Миграция на PostgreSQL и настройка доступа с разных устройств

## Шаг 1: Установка PostgreSQL

### Windows:
1. Скачайте PostgreSQL с официального сайта: https://www.postgresql.org/download/windows/
2. Установите (запомните пароль для пользователя `postgres`)
3. PostgreSQL будет запущен как служба Windows

### Mac:
```bash
brew install postgresql@14
brew services start postgresql@14
```

### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

## Шаг 2: Создание базы данных

```bash
# Windows (через psql):
psql -U postgres
CREATE DATABASE bossboard;
\q

# Mac/Linux:
createdb bossboard
```

## Шаг 3: Установка драйвера PostgreSQL

```powershell
# Windows:
cd backend
py -m pip install psycopg2-binary

# Mac/Linux:
cd backend
pip install psycopg2-binary
```

## Шаг 4: Обновление requirements.txt

Раскомментируйте строку в `backend/requirements.txt`:
```txt
psycopg2-binary>=2.9.9
```

## Шаг 5: Настройка .env файла

Создайте/обновите `backend/.env`:

```env
# PostgreSQL connection
DATABASE_URL=postgresql://postgres:ВАШ_ПАРОЛЬ@localhost/bossboard

# Или если PostgreSQL на другом хосте:
# DATABASE_URL=postgresql://postgres:ВАШ_ПАРОЛЬ@192.168.1.100:5432/bossboard

JWT_SECRET_KEY=your-secret-key-change-this-in-production
CIRCLE_API_KEY=your-circle-api-key
CIRCLE_BASE_URL=https://api.circle.com/v1
```

**Важно:** Замените `ВАШ_ПАРОЛЬ` на ваш реальный пароль PostgreSQL!

## Шаг 6: Миграция данных (опционально)

Если у вас уже есть данные в SQLite, можно экспортировать их:

```python
# Скрипт для миграции данных (создайте migrate_data.py в backend/)
# Это базовый пример - может потребоваться доработка под вашу структуру
```

Или просто начните с чистой базы - таблицы создадутся автоматически при первом запуске.

## Шаг 7: Настройка для доступа с разных устройств

### Обновление CORS в backend/main.py

Обновите `allow_origins` чтобы разрешить доступ с разных IP:

```python
# В backend/main.py, строка 17:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для разработки - разрешает все источники
    # Или укажите конкретные IP:
    # allow_origins=[
    #     "http://localhost:8001",
    #     "http://192.168.1.100:8001",  # IP вашего компьютера в локальной сети
    #     "http://your-domain.com"
    # ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Узнайте ваш IP адрес

**Windows:**
```powershell
ipconfig
# Найдите IPv4 Address (например, 192.168.1.100)
```

**Mac/Linux:**
```bash
ifconfig
# Или
ip addr show
```

### Запуск backend с доступом из сети

Backend уже настроен на `host="0.0.0.0"` (строка 46), что позволяет доступ из сети.

### Настройка frontend для работы с внешним IP

1. **Создайте файл `.env` в папке `src/`:**

```env
# Замените на IP вашего компьютера в локальной сети
API_BASE_URL=http://192.168.1.100:8000/api
```

2. **Или запустите frontend с переменной окружения:**

```powershell
# Windows PowerShell:
$env:API_BASE_URL="http://192.168.1.100:8000/api"
cd src
py frontend.py
```

```bash
# Mac/Linux:
export API_BASE_URL=http://192.168.1.100:8000/api
cd src
python frontend.py
```

## Шаг 8: Настройка файрвола

### Windows:
1. Откройте "Брандмауэр Защитника Windows"
2. Нажмите "Дополнительные параметры"
3. Создайте правило для входящих подключений:
   - Порты: 8000 (backend), 8001 (frontend)
   - Протокол: TCP
   - Действие: Разрешить подключение

### Mac:
```bash
# Разрешить порты через терминал:
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/bin/python3
```

### Linux:
```bash
# UFW:
sudo ufw allow 8000/tcp
sudo ufw allow 8001/tcp
```

## Шаг 9: Запуск

### Терминал 1 - Backend:
```powershell
cd backend
py main.py
```

### Терминал 2 - Frontend:
```powershell
# Установите переменную окружения с вашим IP:
$env:API_BASE_URL="http://ВАШ_IP:8000/api"
cd src
py frontend.py
```

## Доступ с других устройств

### В локальной сети:
- **С телефона/планшета:** `http://ВАШ_IP:8001/login`
- **С другого компьютера:** `http://ВАШ_IP:8001/login`

### Через интернет (требует дополнительной настройки):

1. **Используйте ngrok (быстро, для тестирования):**
   ```bash
   # Установите ngrok: https://ngrok.com/
   ngrok http 8001
   # Получите публичный URL (например: https://abc123.ngrok.io)
   ```

2. **Или настройте порт-форвардинг на роутере:**
   - Откройте порты 8000 и 8001
   - Узнайте ваш внешний IP: https://whatismyipaddress.com/
   - Используйте: `http://ВАШ_ВНЕШНИЙ_IP:8001/login`

3. **Или используйте облачный хостинг:**
   - Heroku, Railway, Render, DigitalOcean и т.д.

## Проверка работы

1. **Backend API:** `http://ВАШ_IP:8000/docs`
2. **Frontend:** `http://ВАШ_IP:8001/login`

## Безопасность

⚠️ **Важно для продакшена:**

1. Не используйте `allow_origins=["*"]` в продакшене
2. Используйте HTTPS (SSL сертификат)
3. Настройте аутентификацию
4. Используйте сильный `JWT_SECRET_KEY`
5. Ограничьте доступ через файрвол
6. Используйте переменные окружения для паролей

## Откат на SQLite (если нужно)

Просто измените `DATABASE_URL` в `.env`:
```env
DATABASE_URL=sqlite:///./bossboard.db
```

И закомментируйте `psycopg2-binary` в `requirements.txt`.

## Troubleshooting

### Ошибка подключения к PostgreSQL:
- Проверьте, что PostgreSQL запущен
- Проверьте пароль в `.env`
- Проверьте, что база данных создана

### Не могу подключиться с другого устройства:
- Проверьте файрвол
- Убедитесь, что используете правильный IP
- Проверьте, что оба устройства в одной сети

### CORS ошибки:
- Обновите `allow_origins` в `backend/main.py`
- Перезапустите backend

