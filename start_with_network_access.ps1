# Скрипт для запуска с доступом из сети
# Ваш IP: 192.168.6.29

Write-Host "🚀 Запуск BossBoard с доступом из сети..." -ForegroundColor Green
Write-Host "📱 IP адрес: 192.168.6.29" -ForegroundColor Cyan
Write-Host ""

# Проверяем, что backend запущен
$backendRunning = netstat -ano | findstr ":8000"
if (-not $backendRunning) {
    Write-Host "⚠️  Backend не запущен! Запустите в отдельном терминале:" -ForegroundColor Yellow
    Write-Host "   cd backend" -ForegroundColor Yellow
    Write-Host "   py main.py" -ForegroundColor Yellow
    Write-Host ""
}

# Устанавливаем переменную окружения для frontend
$env:API_BASE_URL = "http://192.168.6.29:8000/api"

Write-Host "✅ API_BASE_URL установлен: $env:API_BASE_URL" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Доступ с других устройств:" -ForegroundColor Cyan
Write-Host "   http://192.168.6.29:8001/login" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Запуск frontend..." -ForegroundColor Green
Write-Host ""

cd src
py frontend.py

