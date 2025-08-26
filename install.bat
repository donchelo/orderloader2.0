@echo off
echo ==================================================
echo OrderLoader 2.0 - Instalador
echo ==================================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor instala Python 3.8 o superior desde https://python.org
    pause
    exit /b 1
)

echo Python encontrado. Instalando dependencias...
echo.

echo Instalando paquetes principales...
pip install pyautogui==0.9.54
pip install opencv-python==4.8.1.78
pip install pillow==10.0.1
pip install numpy==1.24.3

echo.
echo Instalando paquetes adicionales...
pip install psutil==5.9.5
pip install pywin32==306

echo.
echo Verificando instalación...
python -c "import pyautogui, cv2, PIL, numpy, psutil, win32gui; print('Todas las dependencias instaladas correctamente')"

if errorlevel 1 (
    echo.
    echo ERROR: Algunas dependencias no se instalaron correctamente
    echo Intenta ejecutar: pip install --upgrade pip
    pause
    exit /b 1
)

echo.
echo ==================================================
echo Instalación completada exitosamente!
echo ==================================================
echo.
echo Para ejecutar el sistema:
echo   python main.py
echo.
echo Para ejecutar tests:
echo   python tests/test_remote_desktop.py
echo.
pause
