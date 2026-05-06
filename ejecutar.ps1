# To-Do List Profesional - Script de ejecución para PowerShell
# Autor: Christian Lera

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   📋 TO-DO LIST PROFESIONAL v1.0" -ForegroundColor Yellow
Write-Host "   Autor: Christian Lera" -ForegroundColor Gray
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si Python está instalado
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python no está instalado o no está en el PATH." -ForegroundColor Red
    Write-Host ""
    Write-Host "Por favor, instala Python desde https://python.org" -ForegroundColor Yellow
    Write-Host "Asegúrate de marcar 'Add Python to PATH' durante la instalación." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""
Write-Host "Iniciando la aplicación..." -ForegroundColor Cyan
Write-Host ""

# Ejecutar la aplicación
try {
    python ToDoIt.py
} catch {
    Write-Host ""
    Write-Host "[ERROR] La aplicación ha fallado al ejecutarse." -ForegroundColor Red
    Write-Host "Verifica que el archivo ToDoIt.py existe en esta carpeta." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""
Write-Host "Aplicación cerrada." -ForegroundColor Gray
Read-Host "Presiona Enter para salir"