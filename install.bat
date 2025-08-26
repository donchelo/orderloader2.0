@echo off
echo ========================================
echo OrderLoader 2.0 - Instalador
echo ========================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor instala Python desde https://www.python.org/downloads/
    echo Asegúrate de marcar "Add Python to PATH" durante la instalación
    pause
    exit /b 1
)

echo Python encontrado correctamente
echo.

echo Instalando dependencias...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    echo Intenta ejecutar: pip install --upgrade pip
    pause
    exit /b 1
)

echo.
echo ========================================
echo Instalación completada exitosamente
echo ========================================
echo.
echo Ahora puedes ejecutar launcher.bat para usar OrderLoader 2.0
echo.
pause
