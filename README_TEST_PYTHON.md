# Test Python - Program testowy z GUI

## 📋 Opis

Program do testowania wiedzy z Pythona z przyjaznym interfejsem graficznym. Zawiera **120 pytań** (teoria + kod), z których losowo wybieranych jest 20 na każdy test.

## ✨ Funkcje

- ✅ **Test 20 pytań** - losowy wybór pytań z bazy
- ✅ **Kolorowy feedback** - zielony dla poprawnych, czerwony dla niepoprawnych
- ✅ **Tłumaczenia** - automatyczne wyświetlanie prawidłowej odpowiedzi i wyjaśnienia przy błędzie
- ✅ **Historia testów** - zapisywanie wszystkich testów z datą, wynikiem i czasem
- ✅ **Zakładka teoria** - link do ściągi + szybkie przypomnienia
- ✅ **Przyjemny biały UI** - czytelny i nowoczesny interfejs

## 🚀 Jak uruchomić

### Windows
```bash
py -3 test_python_gui.py
```

### Linux/Mac
```bash
python3 test_python_gui.py
```

## 📁 Pliki

- `test_python_gui.py` - główny program z GUI
- `test_python_baza_pytan.json` - baza pytań (**120 pytań**)
- `test_python_historia.json` - historia testów (tworzy się automatycznie)
- `SCIAGA_PYTHON.md` - ściąga z teorii (używana w zakładce "Teoria")

## 🎯 Jak używać

1. **Rozpocznij test** - kliknij "▶ Rozpocznij test"
2. **Odpowiadaj na pytania** - wybierz odpowiedź i kliknij "✓ Zatwierdź odpowiedź"
3. **Zobacz wynik** - natychmiastowy feedback z tłumaczeniem (jeśli źle)
4. **Następne pytanie** - kliknij "⏭ Następne pytanie"
5. **Sprawdź historię** - zakładka "📊 Historia" pokazuje wszystkie testy

## 📊 Tematy w bazie pytań

- **OOP** (klasy, obiekty, dziedziczenie, metody magiczne, `self`, `super`, polimorfizm, klasy abstrakcyjne, statyczne, wielodziedziczenie) - **28 pytań**
- **Wyjątki** (`try/except/finally/else`, `raise`, własne wyjątki, typowe błędy) - **18 pytań**
- **Podstawy Pythona** (typy, operatory, mutowalność, `==` vs `is`, stringi, listy, tuple, set, dict) - **22 pytania**
- **Moduły i pakiety** (`import`, `from`, `as`, `if __name__ == "__main__"`) - **6 pytań**
- **Funkcje** (`def`, `lambda`, `*args`, `**kwargs`, argumenty domyślne) - **8 pytań**
- **Wielowątkowość** (`threading`, GIL, wątki vs procesy) - **6 pytań**
- **Multiprocessing** (`multiprocessing`, Windows requirements) - **5 pytań**
- **Sieć** (`socket`, TCP/UDP, serwer/klient) - **5 pytań**
- **NumPy** (tablice, operacje elementowe, `shape`, `zeros`) - **6 pytań**
- **Web** (Flask, `@app.route()`, serwery webowe) - **3 pytania**
- **Pliki** (`open()`, `with`, tryby `r/w/a`, `.readlines()`) - **5 pytań**
- **Testowanie** (`unittest`, `assertEqual`, TDD) - **3 pytania**
- **Serializacja** (JSON `dumps/loads`, pickle, ograniczenia) - **4 pytania**
- **Asyncio** (`async/await`, `asyncio.run()`, coroutines) - **3 pytania**
- **List comprehension** (proste, zagnieżdżone, z filtrem) - **4 pytania**
- **Programowanie funkcyjne** (`map`, `filter`, `reduce`, `lambda`) - **4 pytania**
- **Dekoratory** (`@dekorator`, `wrapper`, `@staticmethod`, `@classmethod`) - **5 pytań**
- **Generatory** (`yield`, iteracja przez generator) - **2 pytania**

**Łącznie: 120 pytań** (losowo wybierane 20 na test)

## 🔧 Wymagania

- Python 3.6+
- tkinter (zwykle wbudowany w Python)

Jeśli tkinter nie jest zainstalowany:
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **Windows**: zwykle jest wbudowany
- **Mac**: zwykle jest wbudowany

## 📝 Format pytań

Każde pytanie w `test_python_baza_pytan.json` ma:
- `id` - unikalny numer
- `typ` - "teoria" lub "kod"
- `pytanie` - tekst pytania
- `odpowiedzi` - lista 4 odpowiedzi
- `prawidlowa` - indeks prawidłowej odpowiedzi (0-3)
- `tlumaczenie` - wyjaśnienie dlaczego ta odpowiedź jest prawidłowa

Możesz edytować `test_python_baza_pytan.json` aby dodać własne pytania!

## 🎨 Kolory

- **Zielony** (#2d5016) - poprawna odpowiedź
- **Czerwony** (#8b1a1a) - niepoprawna odpowiedź
- **Biały** (#ffffff) - tło główne
- **Szary** (#f5f5f5) - tło sekcji

---

**Powodzenia na zaliczeniu! 🍀**


