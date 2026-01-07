# 📘 ŚCIĄGA – Python (zaliczenie)

> **Pokrycie tematyczne wykładów W1–W11 względem testu: 100% (14/14 tematów)**  
> Ściąga uporządkowana według ważności tematów w teście (liczba wystąpień pytań)

---

## 🎯 Najważniejsze tematy w teście (kolejność według częstości)

1. **OOP (klasy, obiekty)** – 17 pytań
2. **Wyjątki** – 12 pytań
3. **Podstawy Pythona** – 8 pytań
4. **Moduły i pakiety** – 6 pytań
5. **Funkcje** – 4 pytania
6. **Wielowątkowość/Multiprocessing/Sieć/NumPy** – po 4 pytania
7. **Web** – 3 pytania
8. **Pliki/Testowanie/Serializacja** – po 2 pytania
9. **Asyncio** – 1 pytanie

---

## 1. ⭐ PROGRAMOWANIE OBIEKTOWE (OOP) – 17 pytań w teście

### Klasa i obiekt
```python
class Osoba:
    def __init__(self, imie, nazwisko):
        self.imie = imie
        self.nazwisko = nazwisko

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"

p = Osoba("Anna", "Nowak")
print(p)  # Anna Nowak
```

### `self` – referencja do bieżącego obiektu
```python
class Samochod:
    def __init__(self, marka):
        self.marka = marka  # self.atrybut = wartość
    
    def info(self):
        return f"Marka: {self.marka}"  # dostęp przez self
```

### Metody specjalne (magiczne)
| Metoda | Opis | Przykład użycia |
|--------|------|-----------------|
| `__init__(self, ...)` | konstruktor (tworzenie obiektu) | `obj = Klasa()` |
| `__str__(self)` | reprezentacja tekstowa | `print(obj)` |
| `__repr__(self)` | reprezentacja dla deweloperów | `repr(obj)` |
| `__len__(self)` | długość obiektu | `len(obj)` |
| `__eq__(self, other)` | porównanie równości | `obj1 == obj2` |

```python
class Ksiazka:
    def __init__(self, tytul, strony):
        self.tytul = tytul
        self.strony = strony
    
    def __str__(self):
        return f"'{self.tytul}'"
    
    def __len__(self):
        return self.strony

k = Ksiazka("Python", 300)
print(k)      # 'Python' (używa __str__)
print(len(k)) # 300 (używa __len__)
```

### Dziedziczenie
```python
class Zwierze:
    def __init__(self, gatunek):
        self.gatunek = gatunek
    
    def dzwiek(self):
        return "Dźwięk zwierzęcia"

class Pies(Zwierze):  # Pies dziedziczy po Zwierze
    def __init__(self, rasa):
        super().__init__("pies")  # wywołanie konstruktora klasy bazowej
        self.rasa = rasa
    
    def dzwiek(self):  # nadpisanie metody
        return "Hau!"
```

### `super()` – wywołanie metody klasy bazowej
```python
class Rodzic:
    def __init__(self, x):
        self.x = x

class Dziecko(Rodzic):
    def __init__(self, x, y):
        super().__init__(x)  # wywołanie __init__ z klasy bazowej
        self.y = y
```

### Klasy abstrakcyjne
```python
from abc import ABC, abstractmethod

class Ksztalt(ABC):
    @abstractmethod
    def pole(self):
        pass  # musi być zdefiniowane w klasie potomnej

class Kwadrat(Ksztalt):
    def pole(self):
        return self.bok ** 2
```

### Atrybuty klas vs atrybuty instancji
```python
class Klasa:
    atrybut_klasy = "wspólny dla wszystkich"  # atrybut klasy
    
    def __init__(self, x):
        self.atrybut_instancji = x  # atrybut instancji
```

---

## 2. ⭐ OBSŁUGA WYJĄTKÓW – 12 pytań w teście

### Blok `try` / `except` / `else` / `finally`
```python
try:
    wynik = 10 / 0
except ZeroDivisionError:
    print("Błąd: Dzielenie przez zero!")
except TypeError:
    print("Błąd: Nieprawidłowy typ")
except Exception as e:
    print(f"Inny błąd: {e}")
else:
    print("Sukces:", wynik)  # wykonuje się tylko gdy NIE było wyjątku
finally:
    print("Zawsze się wykonuje")  # wykonuje się zawsze
```

### Typowe wyjątki w Pythonie
| Wyjątek | Kiedy występuje |
|---------|-----------------|
| `ZeroDivisionError` | dzielenie przez zero: `10 / 0` |
| `TypeError` | niekompatybilne typy: `"5" + 5` |
| `ValueError` | nieprawidłowa wartość: `int("abc")` |
| `IndexError` | indeks poza zakresem: `lista[10]` gdy lista ma 3 elementy |
| `KeyError` | brak klucza w słowniku: `dct["nieistnieje"]` |
| `AttributeError` | brak atrybutu: `obj.nieistniejacy` |
| `ImportError` / `ModuleNotFoundError` | brak modułu: `import nieistnieje` |
| `FileNotFoundError` | brak pliku: `open("nieistnieje.txt")` |

### Rzucanie wyjątku (`raise`)
```python
if wiek < 18:
    raise ValueError("Wiek musi być >= 18")
```

### Własny wyjątek
```python
class MojBlad(Exception):
    def __init__(self, message):
        self.message = message

raise MojBlad("Coś poszło nie tak")
```

---

## 3. ⭐ PODSTAWY PYTHONA – 8 pytań w teście

### Typy danych
```python
x = 10          # int
y = 3.14        # float
s = "tekst"     # str
b = True        # bool (True/False)
lst = [1, 2, 3] # list (mutowalna)
tpl = (1, 2)    # tuple (niemutowalna)
dct = {"a": 1}  # dict (słownik)
st = {1, 2, 3}  # set (zbiór)
```

### Operatory
| Operator | Znaczenie | Przykład |
|----------|-----------|----------|
| `//` | dzielenie całkowite | `10 // 3` → `3` |
| `%` | reszta z dzielenia (modulo) | `10 % 3` → `1` |
| `**` | potęgowanie | `2 ** 3` → `8` |
| `==` | porównanie wartości | `5 == 5` → `True` |
| `!=` | różne | `5 != 3` → `True` |
| `is` | porównanie tożsamości | `a is b` (ten sam obiekt?) |
| `and`, `or`, `not` | operatory logiczne | `True and False` → `False` |

### Instrukcje warunkowe
```python
if warunek:
    pass
elif inny_warunek:
    pass
else:
    pass
```

### Pętle
```python
# for
for i in range(5):       # 0, 1, 2, 3, 4
    print(i)

for element in lista:    # iteracja po elementach
    print(element)

# while
while warunek:
    break      # przerwij pętlę
    continue   # przejdź do następnej iteracji
```

### Mutable vs Immutable
- **Mutable** (można zmieniać): `list`, `dict`, `set`
- **Immutable** (nie można zmieniać): `int`, `float`, `str`, `tuple`, `frozenset`

### `==` vs `is`
```python
a = [1, 2]
b = [1, 2]
c = a

a == b   # True (te same wartości)
a is b   # False (różne obiekty w pamięci)
a is c   # True (ten sam obiekt)
```

---

## 4. ⭐ MODUŁY I PAKIETY – 6 pytań w teście

### Import modułu
```python
import math                    # import całego modułu
from math import sqrt, pi      # import konkretnych funkcji
from os import path as ospath  # import z aliasem
```

### Tworzenie własnego modułu
**Plik `moja_klasa.py`:**
```python
class MojaKlasa:
    def __init__(self, x):
        self.x = x

print("To się wykonuje przy imporcie")
```

**Plik `main.py`:**
```python
from moja_klasa import MojaKlasa
obj = MojaKlasa(42)
```

### `if __name__ == "__main__":`
Kod wykonuje się **tylko** przy bezpośrednim uruchomieniu pliku (nie przy imporcie):
```python
def funkcja():
    print("Zawsze dostępna")

if __name__ == "__main__":
    print("Uruchomiono jako skrypt")  # tylko gdy: python main.py
```

---

## 5. FUNKCJE – 4 pytania w teście

### Definicja funkcji
```python
def dodaj(a, b):
    """Dokumentacja funkcji (docstring)."""
    return a + b

wynik = dodaj(2, 3)  # 5
```

### Argumenty domyślne
```python
def powitanie(imie="Gość"):
    print(f"Cześć {imie}!")

powitanie()        # Cześć Gość!
powitanie("Jan")   # Cześć Jan!
```

### `*args` i `**kwargs`
```python
def fun(a, b=10, *args, **kwargs):
    print(a, b)           # 1 2
    print(args)           # (3, 4) - krotka dodatkowych pozycyjnych
    print(kwargs)         # {'x': 5} - słownik dodatkowych nazwanych

fun(1, 2, 3, 4, x=5)
```

### Funkcje lambda (anonimowe)
```python
kwadrat = lambda x: x ** 2
print(kwadrat(5))  # 25

# używane często z map, filter
list(map(lambda x: x*2, [1, 2, 3]))  # [2, 4, 6]
```

---

## 6. WIELOWĄTKOWOŚĆ I WIELOPROCESOWOŚĆ – 4 pytania w teście

### Wątki (`threading`)
```python
import threading
import time

def zadanie(n):
    print(f"Wątek {n} rozpoczął")
    time.sleep(2)
    print(f"Wątek {n} zakończył")

watki = []
for i in range(3):
    w = threading.Thread(target=zadanie, args=(i,))
    watki.append(w)
    w.start()

for w in watki:
    w.join()  # czekaj na zakończenie

print("Wszystkie wątki zakończone")
```

### Procesy (`multiprocessing`)
```python
import multiprocessing

def zadanie(n):
    print(f"Proces {n}")

# UWAGA: wymagane na Windows!
if __name__ == "__main__":
    procesy = []
    for i in range(3):
        p = multiprocessing.Process(target=zadanie, args=(i,))
        procesy.append(p)
        p.start()
    
    for p in procesy:
        p.join()
```

> **⚠️ Ważne:** `multiprocessing` wymaga `if __name__ == "__main__":` na Windows!

---

## 7. KOMUNIKACJA SIECIOWA (socket) – 4 pytania w teście

### Serwer TCP
```python
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 12345))
server.listen(1)  # maksymalna liczba połączeń w kolejce

print("Serwer oczekuje...")
conn, addr = server.accept()  # akceptuj połączenie

dane = conn.recv(1024)        # odbierz dane (max 1024 bajty)
print(f"Otrzymano: {dane.decode()}")

conn.sendall(b"Odpowiedz")    # wyślij odpowiedź
conn.close()
```

### Klient TCP
```python
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 12345))

client.sendall(b"Wiadomosc")
odpowiedz = client.recv(1024)
print(f"Odpowiedz: {odpowiedz.decode()}")

client.close()
```

---

## 8. NUMPY (tablice numeryczne) – 4 pytania w teście

```python
import numpy as np

arr = np.array([1, 2, 3])      # tablica 1D
print(arr * 2)                  # [2 4 6] - operacje na całej tablicy
print(arr.shape)                # (3,) - kształt tablicy

# Tworzenie tablic
np.zeros((2, 3))                # macierz 2x3 zer
np.ones((2, 3))                 # macierz 2x3 jedynek
np.array([[1, 2], [3, 4]])      # macierz 2x2

# NumPy != list (array i matrix to NIE to samo w Pythonie)
lista = [1, 2, 3]
tablica = np.array([1, 2, 3])
```

---

## 9. WEB (Flask/Django) – 3 pytania w teście

### Flask (mikro-framework)
```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)
```

### Popularne frameworki webowe w Pythonie
- **Flask** – mikro-framework
- **Django** – pełny framework

---

## 10. PRACA Z PLIKAMI – 2 pytania w teście

### Odczyt / zapis
```python
# Odczyt
with open("plik.txt", "r", encoding="utf-8") as f:
    zawartosc = f.read()          # cały plik
    # lub
    linie = f.readlines()         # lista linii

# Zapis
with open("plik.txt", "w", encoding="utf-8") as f:
    f.write("Hello\n")
    f.writelines(["Linia 1\n", "Linia 2\n"])
```

### Tryby otwarcia pliku
| Tryb | Opis |
|------|------|
| `r` | odczyt (domyślny dla tekstu) |
| `w` | zapis (nadpisuje istniejący plik) |
| `a` | dopisywanie (append) |
| `rb` / `wb` | tryb binarny (dla plików binarnych) |
| `x` | zapis (błąd jeśli plik istnieje) |

> **Uwaga:** `with open()` automatycznie zamyka plik po wyjściu z bloku!

---

## 11. TESTOWANIE (`unittest`) – 2 pytania w teście

```python
import unittest

def dodaj(a, b):
    return a + b

class TestDodaj(unittest.TestCase):
    def test_suma(self):
        self.assertEqual(dodaj(2, 3), 5)
    
    def test_ujemne(self):
        self.assertNotEqual(dodaj(-1, 1), -1)

if __name__ == "__main__":
    unittest.main()
```

### Metody asercji
- `self.assertEqual(a, b)` – sprawdza czy `a == b`
- `self.assertNotEqual(a, b)` – sprawdza czy `a != b`
- `self.assertTrue(x)` – sprawdza czy `x` jest `True`
- `self.assertFalse(x)` – sprawdza czy `x` jest `False`
- `self.assertRaises(Error, func, args)` – sprawdza czy funkcja rzuca wyjątek

### TDD (Test Driven Development)
**Tak, w Pythonie możliwa jest realizacja TDD!** Używa się `unittest` lub `pytest`.

---

## 12. SERIALIZACJA (JSON, pickle) – 2 pytania w teście

### JSON
```python
import json

dane = {"imie": "Jan", "wiek": 30}

# Do stringa
json_str = json.dumps(dane)        # '{"imie": "Jan", "wiek": 30}'

# Z powrotem do dict
dane2 = json.loads(json_str)       # {"imie": "Jan", "wiek": 30}

# Z/do pliku
with open("dane.json", "w") as f:
    json.dump(dane, f)

with open("dane.json", "r") as f:
    dane_odczyt = json.load(f)
```

### Pickle (obiekty Pythona)
```python
import pickle

dane = {"a": 1, "b": [1, 2, 3]}

# Zapis
with open("dane.pkl", "wb") as f:  # tryb binarny!
    pickle.dump(dane, f)

# Odczyt
with open("dane.pkl", "rb") as f:
    dane_odczyt = pickle.load(f)
```

---

## 13. ASYNCHRONICZNOŚĆ (`asyncio`) – 1 pytanie w teście

```python
import asyncio

async def zadanie():
    print("Start")
    await asyncio.sleep(1)  # czekaj 1 sekundę (nie blokuje!)
    print("Koniec")

asyncio.run(zadanie())
```

---

## 📌 Dodatkowe tematy (wykłady, ale NIE w teście)

### Programowanie funkcyjne (map, filter, reduce)
```python
from functools import reduce

list(map(lambda x: x*2, [1, 2, 3]))        # [2, 4, 6]
list(filter(lambda x: x > 0, [-1, 0, 2]))  # [2]
reduce(lambda a, b: a + b, [1, 2, 3])      # 6

# List comprehension (często lepsze niż map/filter)
[x**2 for x in range(5)]                    # [0, 1, 4, 9, 16]
[x for x in range(10) if x % 2 == 0]       # [0, 2, 4, 6, 8]
```

### Dekoratory
```python
def dekorator(func):
    def wrapper(*args, **kwargs):
        print("Przed funkcją")
        wynik = func(*args, **kwargs)
        print("Po funkcji")
        return wynik
    return wrapper

@dekorator
def powitanie():
    print("Cześć!")
```

### Generatory (`yield`)
```python
def generator():
    yield 1
    yield 2
    yield 3

for val in generator():
    print(val)  # 1, 2, 3
```

---

## 🔑 Najważniejsze słowa kluczowe w Pythonie

| Słowo | Znaczenie |
|-------|-----------|
| `def` | definicja funkcji |
| `class` | definicja klasy |
| `self` | referencja do bieżącego obiektu |
| `import` / `from` | importowanie modułów |
| `return` | zwracanie wartości z funkcji |
| `raise` | rzucanie wyjątku |
| `try` / `except` / `finally` | obsługa wyjątków |
| `with` | kontekst (np. pliki) |
| `lambda` | funkcja anonimowa |
| `pass` | pusta instrukcja (nic nie rób) |
| `None` | brak wartości |
| `True` / `False` | wartości logiczne |
| `if __name__ == "__main__":` | kod wykonywany tylko jako skrypt |

---

## 📌 Częste błędy na teście

1. **`ZeroDivisionError`** – dzielenie przez zero (`10 / 0`)
2. **`TypeError`** – operacja na niekompatybilnych typach (`"5" + 5`)
3. **`IndexError`** – indeks poza zakresem listy
4. **`KeyError`** – brak klucza w słowniku
5. **`AttributeError`** – obiekt nie ma danego atrybutu
6. **`ImportError` / `ModuleNotFoundError`** – brak modułu
7. **`FileNotFoundError`** – brak pliku

---

## 🧠 Szybkie przypomnienia

### Zakres zmiennych (scope)
- **LEGB**: Local → Enclosing → Global → Built-in

### Operatory logiczne
- `and` – "i" (oba muszą być True)
- `or` – "lub" (przynajmniej jeden True)
- `not` – negacja

### `*args` vs `**kwargs`
- `*args` – krotka dodatkowych argumentów pozycyjnych
- `**kwargs` – słownik dodatkowych argumentów nazwanych

### NumPy vs lista
- `array` i `matrix` w Pythonie to **NIE** to samo!
- `numpy.array` to tablica numeryczna, `list` to zwykła lista

### Moduły numeryczne
- **NumPy** – podstawowe tablice numeryczne
- **SciPy** – zaawansowane funkcje numeryczne (całkowanie, optymalizacja, itp.)

---

**Powodzenia na zaliczeniu! 🍀**
