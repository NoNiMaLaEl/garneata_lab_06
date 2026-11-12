# Laborator 6 - Algoritmi Fundamentali

Student: Garneata Dragos  
Proiect Jira (Kanban): `Laborator 6` (`LAB6`)

## Descriere
Aplicatie Python care implementeaza doi algoritmi de sortare crescatoare (**Insertion Sort** si **Merge Sort**) in functii separate, fara utilizarea `sorted()` sau `list.sort()`. La fiecare rulare se citesc strict primele doua linii din `date.txt`, se valideaza datele, se executa exclusiv algoritmul ales, iar rezultatul este scris in acelasi fisier sub cele doua linii initiale.

## Structura proiectului
- `sortari.py` - functiile `insertion_sort`, `merge_sort`, `_interclaseaza` si maparea `ALGORITMI_DISPONIBILI`
- `main.py` - citirea din `date.txt`, validari (`FileNotFoundError`, numere invalide, algoritm necunoscut), selectie algoritm si scrierea rezultatului
- `date.txt` - fisierul de intrare/iesire
- `tests/test_sortari.py` - teste unitare pentru algoritmi si cazurile de validare

## Format `date.txt`
Intrare:
```text
7 8 2 3 4 5
Merge
```

Dupa rulare:
```text
7 8 2 3 4 5
Merge
Merge: 2 3 4 5 7 8
```

## Rulare si testare
```bash
python3 main.py
python3 -m unittest discover -s tests -v
```
