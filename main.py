"""Punct de intrare pentru aplicatia de sortare din Laborator 6.

Citeste exclusiv primele doua linii din `date.txt`, valideaza datele de intrare,
ruleaza doar algoritmul selectat si scrie rezultatul sub liniile initiale.
"""

from pathlib import Path
import sys

from sortari import ALGORITMI_DISPONIBILI


def parseaza_linie_numere(linie_numere: str) -> list[int]:
    """Extrage si valideaza o lista nevida de numere intregi din linia 1.

    Unde: `main.py`, apelata la validarea primei linii din `date.txt`.
    De ce: Separa validarea numerelor de I/O pentru mesaje clare de eroare
    si testare unitara usoara.
    """
    tokenuri = linie_numere.strip().split()
    if not tokenuri:
        raise ValueError("Linia 1 din fisier nu contine niciun numar intreg.")

    numere: list[int] = []
    valori_invalide: list[str] = []
    for token in tokenuri:
        try:
            numere.append(int(token))
        except ValueError:
            valori_invalide.append(token)

    if valori_invalide:
        invalide_str = ", ".join(valori_invalide)
        raise ValueError(f"Linia 1 contine valori care nu sunt numere intregi: {invalide_str}.")

    return numere


def rezolva_fisier(cale_fisier: str | Path = "date.txt") -> tuple[bool, str]:
    """Citeste primele 2 linii din fisier, sorteaza cu algoritmul ales si scrie rezultatul.

    Unde: `main.py`, fluxul principal al aplicatiei.
    De ce: Pastreaza intacte cele doua linii de intrare si previne duplicarea
    rezultatelor la rulari consecutive pe acelasi fisier `date.txt`.
    """
    cale = Path(cale_fisier)
    if not cale.is_file():
        return False, f"Eroare: Fisierul '{cale}' nu exista."

    try:
        linii = cale.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return False, f"Eroare la citirea fisierului '{cale}': {exc}"

    if len(linii) < 2:
        return (
            False,
            f"Eroare: Fisierul '{cale}' trebuie sa contina cel putin 2 linii "
            "(linia 1: numere intregi, linia 2: numele algoritmului).",
        )

    linia_1 = linii[0].rstrip("\r\n")
    linia_2 = linii[1].rstrip("\r\n")

    try:
        numere = parseaza_linie_numere(linia_1)
    except ValueError as exc:
        return False, f"Eroare: {exc}"

    cheie_algoritm = " ".join(linia_2.strip().lower().split())
    if cheie_algoritm not in ALGORITMI_DISPONIBILI:
        nume_afisat = linia_2.strip() or "<gol>"
        return (
            False,
            f"Eroare: Algoritmul '{nume_afisat}' nu este implementat. "
            "Algoritmi disponibili: Insertion, Merge.",
        )

    eticheta, functie_sortare = ALGORITMI_DISPONIBILI[cheie_algoritm]
    sortate = functie_sortare(numere)
    linie_rezultat = f"{eticheta}: {' '.join(str(x) for x in sortate)}"

    # Scriem strict cele 2 linii initiale urmate de rezultatul etichetat.
    continut_nou = f"{linia_1}\n{linia_2}\n{linie_rezultat}\n"
    try:
        cale.write_text(continut_nou, encoding="utf-8")
    except OSError as exc:
        return False, f"Eroare la scrierea in fisierul '{cale}': {exc}"

    return True, linie_rezultat


def main() -> int:
    """Ruleaza procesarea fisierului `date.txt` si afiseaza rezultatul in consola.

    Unde: Entrypoint CLI in `main.py`.
    De ce: Ofera feedback clar in consola indiferent daca datele sunt valide sau nu.
    """
    ok, mesaj = rezolva_fisier("date.txt")
    print(mesaj)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
