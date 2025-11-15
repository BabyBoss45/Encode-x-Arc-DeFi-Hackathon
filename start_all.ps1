# Скрипт для запуска Backend и Frontend одновременно
# ВАЖНО: Запустите backend и frontend в ОТДЕЛЬНЫХ терминалах!

Write-Host "🚀 BossBoard - Команды для запуска" -ForegroundColor Green
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "ТЕРМИНАЛ 1 - Backend:" -ForegroundColor Yellow
Write-Host "  cd backend" -ForegroundColor White
Write-Host "  py main.py" -ForegroundColor White
Write-Host ""
Write-Host "Или используйте скрипт:" -ForegroundColor Gray
Write-Host "  .\start_backend_network.ps1" -ForegroundColor White
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "ТЕРМИНАЛ 2 - Frontend:" -ForegroundColor Yellow
Write-Host "  `$env:API_BASE_URL=`"http://192.168.6.29:8000/api`"" -ForegroundColor White
Write-Host "  cd src" -ForegroundColor White
Write-Host "  py frontend.py" -ForegroundColor White
Write-Host ""
Write-Host "Или используйте скрипт:" -ForegroundColor Gray
Write-Host "  .\start_with_network_access.ps1" -ForegroundColor White
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 После запуска откройте:" -ForegroundColor Green
Write-Host "  http://localhost:8001/login" -ForegroundColor Cyan
Write-Host "  или" -ForegroundColor Gray
Write-Host "  http://192.168.6.29:8001/login" -ForegroundColor Cyan
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "Нажмите любую клавишу для выхода..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

