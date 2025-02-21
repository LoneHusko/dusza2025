---
sidebar_position: 2
---

# Telepítési útmutató

## Fejlesztői környezet beállítása

### 1. Python telepítése

1. Töltse le a Python telepítőt a [python.org](https://python.org) oldalról
2. Futtassa a telepítőt
3. Jelölje be a "Add Python to PATH" opciót
4. Válassza a "Customize installation" opciót
5. Telepítse az összes ajánlott komponenst

### 2. Virtuális környezet létrehozása

```bash
# Virtuális környezet létrehozása
python -m venv venv

# Környezet aktiválása Windows-on
venv\Scripts\activate

# Környezet aktiválása Unix rendszereken
source venv/bin/activate
```

### 3. Függőségek telepítése

```bash
# Függőségek telepítése
pip install -r requirements.txt
```

## IDE beállítása

### PyCharm

1. Nyissa meg a projektet PyCharm-ban
2. Állítsa be a virtuális környezetet:
   - File > Settings > Project > Python Interpreter
   - Add Interpreter > Existing Environment
   - Válassza ki a `venv/Scripts/python.exe` fájlt

### Visual Studio Code

1. Telepítse a Python bővítményt
2. Nyissa meg a projektet
3. Válassza ki a Python interpretert:
   - Ctrl+Shift+P
   - Python: Select Interpreter
   - Válassza a virtuális környezetet

## Fejlesztői eszközök

### Ajánlott bővítmények

1. **PyCharm**
   - Qt Designer
   - Git Integration
   - Python Security

2. **VS Code**
   - Python
   - Pylance
   - Qt Tools
   - Git Lens

## Futtatás és tesztelés

### Program indítása

```bash
python main.pyw
```

## Hibaelhárítás

### Gyakori problémák

1. **ImportError**
   - Ellenőrizze a virtuális környezet aktiválását
   - Telepítse újra a függőségeket
   - Ellenőrizze a Python verziót

2. **Qt hibák**
   - Telepítse újra a PySide6 csomagokat
