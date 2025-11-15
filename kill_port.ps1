# Скрипт для освобождения портов 8000 и 8001

param(
    [int]$Port = 0
)

function Kill-Port {
    param([int]$PortNumber)
    
    Write-Host "🔍 Проверяю порт $PortNumber..." -ForegroundColor Yellow
    
    $connections = netstat -ano | findstr ":$PortNumber" | findstr "LISTENING"
    
    if ($connections) {
        foreach ($conn in $connections) {
            $pid = ($conn -split '\s+')[-1]
            if ($pid -and $pid -ne "0") {
                Write-Host "⚠️  Порт $PortNumber занят процессом $pid. Останавливаю..." -ForegroundColor Yellow
                taskkill /PID $pid /F 2>$null
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "✅ Процесс $pid остановлен" -ForegroundColor Green
                } else {
                    Write-Host "❌ Не удалось остановить процесс $pid (возможно, нет прав)" -ForegroundColor Red
                }
            }
        }
    } else {
        Write-Host "✅ Порт $PortNumber свободен" -ForegroundColor Green
    }
}

if ($Port -ne 0) {
    Kill-Port -PortNumber $Port
} else {
    Write-Host "🛑 Освобождение портов 8000 и 8001..." -ForegroundColor Cyan
    Write-Host ""
    Kill-Port -PortNumber 8000
    Kill-Port -PortNumber 8001
    Write-Host ""
    Write-Host "✅ Готово!" -ForegroundColor Green
}

