"""Algoritmi de sortare crescatoare pentru Laborator 6 (Algoritmi Fundamentali).

Implementeaza Insertion Sort si Merge Sort in functii separate, fara a folosi
functiile built-in sorted() sau list.sort().
"""

from typing import Callable


def insertion_sort(numere: list[int]) -> list[int]:
    """Sorteaza crescator o lista de intregi folosind Insertion Sort.

    Unde: Modulul `sortari.py`, apelata selectiv din `main.py`.
    De ce: Implementare iterativa O(n^2) stabila si eficienta pe liste mici
    sau aproape sortate, lucrand pe o copie pentru a nu altera intrarea.
    """
    rezultat = numere.copy()
    for i in range(1, len(rezultat)):
        cheie = rezultat[i]
        j = i - 1
        while j >= 0 and rezultat[j] > cheie:
            rezultat[j + 1] = rezultat[j]
            j -= 1
        rezultat[j + 1] = cheie
    return rezultat


def _interclaseaza(stanga: list[int], dreapta: list[int]) -> list[int]:
    """Interclaseaza doua liste deja sortate crescator intr-o singura lista.

    Unde: Functie helper interna in `sortari.py`, folosita de `merge_sort`.
    De ce: Izoleaza pasul de combinare din strategia Divide et Impera.
    """
    rezultat: list[int] = []
    i = 0
    j = 0
    while i < len(stanga) and j < len(dreapta):
        if stanga[i] <= dreapta[j]:
            rezultat.append(stanga[i])
            i += 1
        else:
            rezultat.append(dreapta[j])
            j += 1
    rezultat.extend(stanga[i:])
    rezultat.extend(dreapta[j:])
    return rezultat


def merge_sort(numere: list[int]) -> list[int]:
    """Sorteaza crescator o lista de intregi folosind Merge Sort.

    Unde: Modulul `sortari.py`, apelata selectiv din `main.py`.
    De ce: Ofera complexitate garantata O(n log n) in toate cazurile prin
    strategie Divide et Impera, fara a utiliza sorted() sau list.sort().
    """
    if len(numere) <= 1:
        return numere.copy()

    mijloc = len(numere) // 2
    stanga = merge_sort(numere[:mijloc])
    dreapta = merge_sort(numere[mijloc:])
    return _interclaseaza(stanga, dreapta)


# Mapare unica intre numele normalizat al algoritmului, eticheta de iesire si functie.
ALGORITMI_DISPONIBILI: dict[str, tuple[str, Callable[[list[int]], list[int]]]] = {
    "insertion": ("Insertion", insertion_sort),
    "insertion sort": ("Insertion", insertion_sort),
    "merge": ("Merge", merge_sort),
    "merge sort": ("Merge", merge_sort),
}
