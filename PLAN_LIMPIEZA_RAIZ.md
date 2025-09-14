# 🧹 Plan de Limpieza de Carpeta Raíz

## 📋 **Estado Actual (Problemas)**

La carpeta raíz está completamente desordenada con:

### **❌ Redundancias Identificadas:**
- **3 versiones del sistema**: `main.py`, `main_simplified.py`, `main_ultra_simple.py`
- **3 configuraciones**: `config.py`, `config_simple.py`, `config.py` (en orderloader_clean)
- **3 requirements**: `requirements.txt`, `requirements_simple.txt`, `requirements.txt` (en orderloader_clean)
- **3 READMEs**: `README.md`, `README_SIMPLE.md`, `README.md` (en orderloader_clean)
- **15+ archivos de test**: `test_*.py` dispersos
- **8 archivos de documentación**: Múltiples archivos .md
- **2 instaladores**: `install.bat`, `install_simple.bat`

### **❌ Carpetas Redundantes:**
- `src/` (versión original)
- `orderloader_clean/` (versión compleja)
- `orderloader_final/` (versión consolidada) ← **ESTA ES LA BUENA**

---

## 🎯 **Plan de Limpieza**

### **Paso 1: Identificar qué mantener**
- ✅ **`orderloader_final/`** - Versión consolidada y limpia
- ✅ **`assets/`** - Imágenes originales (para referencia)
- ✅ **`queues/`** - Datos existentes
- ✅ **`claude.md`** - Documentación original

### **Paso 2: Eliminar redundancias**
- ❌ **`src/`** - Versión original (redundante)
- ❌ **`orderloader_clean/`** - Versión compleja (redundante)
- ❌ **`main.py`** - Versión original (redundante)
- ❌ **`main_simplified.py`** - Versión simplificada (redundante)
- ❌ **`main_ultra_simple.py`** - Versión ultra simple (redundante)
- ❌ **`config_simple.py`** - Configuración simple (redundante)
- ❌ **`requirements_simple.txt`** - Requirements simple (redundante)
- ❌ **`README_SIMPLE.md`** - README simple (redundante)
- ❌ **`test_*.py`** - Tests dispersos (redundantes)
- ❌ **`install*.bat`** - Instaladores (redundantes)
- ❌ **Documentación redundante** - Múltiples archivos .md

### **Paso 3: Reorganizar estructura final**
```
orderLoader2.0/
├── 📁 orderloader_final/         # Sistema principal (RENOMBRAR A orderloader/)
├── 📁 assets/                    # Imágenes originales
├── 📁 queues/                    # Datos existentes
├── 📄 claude.md                  # Documentación original
├── 📄 README.md                  # Documentación principal
└── 📄 .gitignore                 # Archivos a ignorar
```

---

## 🚀 **Acciones a Ejecutar**

1. **Renombrar** `orderloader_final/` → `orderloader/`
2. **Eliminar** todas las carpetas y archivos redundantes
3. **Crear** README.md principal que apunte a `orderloader/`
4. **Limpiar** archivos temporales y logs
5. **Verificar** que todo funciona correctamente

---

## ✅ **Resultado Esperado**

Una carpeta raíz limpia con:
- **1 sistema principal** - `orderloader/`
- **1 documentación** - `README.md`
- **Datos existentes** - `assets/`, `queues/`
- **Sin redundancias** - Solo lo esencial
