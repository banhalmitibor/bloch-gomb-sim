# Bloch-gömb Szimulátor

Ez a projekt a BME **Kvantuminformatikai alkalmazások** tárgyára készült. A program egy interaktív, 3D-s webes felületen jeleníti meg a kvantumállapotokat (qubiteket) a Bloch-gömbön, és lehetővé teszi különböző kvantumkapuk és forgatások vizuális tesztelését.

## Főbb funkciók
* **3D Interaktív vizualizáció:** Qubitek állapotának valós idejű ábrázolása a Bloch-gömbön.
* **Alapvető kvantumkapuk:** Hadamard (H), Pauli (X, Y, Z), valamint fáziskapuk (S, T) alkalmazása.
* **Szabad forgatások:** Tetszőleges szögű forgatás az X, Y és Z tengelyek körül (Rx, Ry, Rz).
* **Láncolt kapuk:** Több kapuból álló láncok rögzítése, elnevezése és újrahasználata egyetlen gombnyomással.
* **Több állapotvektor kezelése:** Egyszerre több állapotvektor létrehozása és összehasonlítása különböző színekkel.

---

## Futtatás és Indítás

A szimulátort kétféleképpen lehet elindítani, attól függően, hogy rendelkezel-e Python fejlesztői környezettel.

### 1. Futtatás önálló programként (standalone futtatás)
Ez a módszer olyan Windows-os gépeken is működik, ahol nincs telepítve a Python.

1. Navigálj a projekt `dist` mappájába.
2. Kattints duplán a **`BlochSimulator.exe`** fájlra.
3. Megnyílik egy parancssor a háttérben, majd 2-3 másodperc múlva automatikusan betölt a szimulátor az alapértelmezett böngésződben.

### 2. Futtatás forráskódból (Továbbfejlesztés révén)
Ha szeretnéd a kódot szerkeszteni, vagy Python környezetből (pl. Linux/Mac alatt) futtatni, az alábbi lépéseket kövesd.

#### Követelmények
A futtatáshoz Python 3.8+ és a következő csomagok szükségesek:
* `streamlit`
* `numpy`
* `plotly`

A függőségek telepítése terminálból:
* `pip install streamlit numpy plotly`

#### Futtatás
Ha a követelmények sikeresen ki vannak elégítve, akkor a gyökérmappából kiadva az alábbi parancsot indítható a program:
* `streamlit run app.py`


