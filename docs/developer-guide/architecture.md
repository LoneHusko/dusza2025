---
sidebar_position: 1
---

# Rendszer architektúra

## Áttekintés

A Dusza2025 rendszer moduláris felépítésű, három fő komponensre osztva:

```
dusza2025/
├── main.pyw           # Főprogram
├── requirements.txt   # Függőségek
├── widgets/           # GUI komponensek
│   ├── home.py
│   ├── computer_manage.py
│   └── program_manage.py
└── modules/          # Üzleti logika
    └── models.py
```

## Komponensek

### Főprogram (`main.pyw`)

A főprogram felelős a következőkért:
- Alkalmazás belépési pont
- GUI főablak implementáció
- Navigációs rendszer
- Widget kezelés és életciklus

### Widgetek (`widgets/`)

A felhasználói felület komponensei:

#### `home.py`
- Főoldal megjelenítése
- Rendszerállapot áttekintése

#### `computer_manage.py`
- Számítógép hozzáadása
- Számítógép törlése

#### `program_manage.py`
- Program módosítása
- Program végleges leállítása
- Új folyamat indítása
- Folyamat keresése
- Folyamat leállítása

### Modulok (`modules/`)

#### `models.py`
- Adatmodellek
- Üzleti logika
- Adatkezelés

## Architektúrális döntések

### GUI Framework

A rendszer a **PySide6** (Qt for Python) keretrendszert használja:
- Modern, gyors GUI megjelenítés
- Platformfüggetlen működés
- Gazdag widget készlet
- Python integráció

### Adatkezelés

- Fájl alapú konfiguráció tárolás
- JSON formátum használata
- Moduláris adatstruktúrák
