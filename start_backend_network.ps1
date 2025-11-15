# Скрипт для запуска backend с доступом из сети

Write-Host "🚀 Запуск BossBoard Backend..." -ForegroundColor Green
Write-Host "📱 IP адрес: 192.168.6.29" -ForegroundColor Cyan
Write-Host ""

cd backend

# Проверяем наличие .env файла
if (-not (Test-Path .env)) {
    Write-Host "📝 Создаю .env файл..." -ForegroundColor Yellow
    @"
DATABASE_URL=sqlite:///./bossboard.db
JWT_SECRET_KEY=my-secret-key-change-in-production
CIRCLE_API_KEY=test-key
CIRCLE_BASE_URL=https://api.circle.com/v1
CORS_ORIGINS=*
"@ | Out-File -FilePath .env -Encoding utf8
    Write-Host "✅ .env файл создан" -ForegroundColor Green
} else {
    # Обновляем CORS_ORIGINS если нужно
    $envContent = Get-Content .env -Raw
    if ($envContent -notmatch "CORS_ORIGINS") {
        Write-Host "📝 Добавляю CORS_ORIGINS в .env..." -ForegroundColor Yellow
        Add-Content .env "`nCORS_ORIGINS=*"
    }
}

# Проверяем и освобождаем порт 8000 если занят
Write-Host "🔍 Проверяю порт 8000..." -ForegroundColor Yellow
$port8000 = netstat -ano | findstr ":8000" | findstr "LISTENING"
if ($port8000) {
    $pid = ($port8000 -split '\s+')[-1]
    Write-Host "⚠️  Порт 8000 занят процессом $pid. Останавливаю..." -ForegroundColor Yellow
    taskkill /PID $pid /F 2>$null
    Start-Sleep -Seconds 1
    Write-Host "✅ Порт освобожден" -ForegroundColor Green
}

Write-Host ""
Write-Host "🌐 Backend будет доступен по адресу:" -ForegroundColor Cyan
Write-Host "   http://192.168.6.29:8000" -ForegroundColor White
Write-Host "   http://localhost:8000" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Запуск backend..." -ForegroundColor Green
Write-Host ""

py main.py

