# Dusza2025 Folyamatkezelő Rendszer

A Dusza2025 egy folyamatkezelő rendszer, ami a Dusza Árpád hagyományos programozóversenyre készült. A rendszer lehetővé teszi számítógépek és programok központosított kezelését egy klaszteren belül.

## Főbb funkciók

- **Számítógép menedzsment**: Gépek hozzáadása és eltávolítása a klaszterből
- **Program kezelés**: Programok futtatása, módosítása és leállítása
- **Folyamat monitorozás**: Aktív folyamatok keresése és leállítása
- **Központosított irányítás**: Egységes felület minden művelethez

## Gyors kezdés

1. Indítsa el a `main.exe` fájlt
2. A megjelenő ablakban válassza ki a klaszter mappát
3. A sikeres indítás után megjelenik a főablak

## Fejlesztői környezet beállítása

```bash
# Virtuális környezet létrehozása
python -m venv venv

# Környezet aktiválása Windows-on
venv\Scripts\activate
# VAGY Unix rendszereken
source venv/bin/activate

# Függőségek telepítése
pip install -r requirements.txt

# Program indítása
python main.pyw
```

## Dokumentáció

A dokumentáció két formában érhető el:

- **Web felület**: [https://dusza2025.pages.dev](https://dusza2025.pages.dev)
- **Markdown fájlok**: A `/docs` mappában található markdown fájlok

## Licenc

[MIT License](LICENSE)
