@echo off
title To-Do List Profesional
echo ========================================
echo    📋 TO-DO LIST PROFESIONAL v1.0
echo    Autor: Christian Lera
echo ========================================
echo.
echo Verificando Python...

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en el PATH.
    echo.
    echo Por favor, instala Python desde https://python.org
    echo Asegurate de marcar "Add Python to PATH" durante la instalacion.
    echo.
    pause
    exit /b 1
)

echo Python encontrado!
echo.
echo Iniciando la aplicacion...
echo.

python ToDoIt.py

if errorlevel 1 (
    echo.
    echo [ERROR] La aplicacion ha fallado al ejecutarse.
    echo Verifica que el archivo ToDoIt.py existe.
    echo.
)

echo.
echo Aplicacion cerrada.
pause