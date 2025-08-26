@echo off
echo ==================================================
echo OrderLoader 2.0 - Instalador Mejorado
echo ==================================================
echo.

echo Instalando dependencias mejoradas...
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor instala Python 3.7+ desde https://python.org
    pause
    exit /b 1
)

echo Python encontrado. Instalando dependencias...
echo.

REM Actualizar pip
echo [1/6] Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias principales
echo [2/6] Instalando dependencias principales...
pip install pyautogui opencv-python pillow numpy

REM Instalar dependencias adicionales para mejoras
echo [3/6] Instalando dependencias adicionales...
pip install psutil pywin32

REM Verificar instalación
echo [4/6] Verificando instalación...
python -c "import pyautogui, cv2, PIL, numpy, psutil, win32gui; print('Todas las dependencias instaladas correctamente')"

if errorlevel 1 (
    echo ERROR: Algunas dependencias no se instalaron correctamente
    pause
    exit /b 1
)

REM Crear directorios necesarios
echo [5/6] Creando directorios...
if not exist "reference_images" mkdir reference_images
if not exist "logs" mkdir logs

REM Verificar archivos de configuración
echo [6/6] Verificando archivos de configuración...
if not exist "config.py" (
    echo ERROR: config.py no encontrado
    pause
    exit /b 1
)

if not exist "main.py" (
    echo ERROR: main.py no encontrado
    pause
    exit /b 1
)

echo.
echo ==================================================
echo INSTALACIÓN COMPLETADA EXITOSAMENTE
echo ==================================================
echo.
echo Mejoras implementadas:
echo - Gestor avanzado de escritorio remoto
echo - Múltiples estrategias de activación
echo - Sistema de recuperación automática
echo - Verificación visual mejorada
echo - Logging detallado
echo.
echo Para probar las mejoras:
echo 1. python test_remote_desktop_improved.py
echo 2. python main.py
echo.
echo Para diagnóstico:
echo python diagnostic.py
echo.
pause
