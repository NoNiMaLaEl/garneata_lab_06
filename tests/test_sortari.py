"""Teste unitare pentru algoritmii de sortare si procesarea fisierului date.txt."""

import ast
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from main import parseaza_linie_numere, rezolva_fisier
from sortari import insertion_sort, merge_sort


class TestSortari(unittest.TestCase):
    """Teste pentru Insertion Sort si Merge Sort."""

    def test_insertion_sort_cazuri_standard_si_limita(self) -> None:
        self.assertEqual(insertion_sort([7, 8, 2, 3, 4, 5]), [2, 3, 4, 5, 7, 8])
        self.assertEqual(insertion_sort([]), [])
        self.assertEqual(insertion_sort([42]), [42])
        self.assertEqual(insertion_sort([5, -3, 0, -3, 10]), [-3, -3, 0, 5, 10])

    def test_merge_sort_cazuri_standard_si_limita(self) -> None:
        self.assertEqual(merge_sort([7, 8, 2, 3, 4, 5]), [2, 3, 4, 5, 7, 8])
        self.assertEqual(merge_sort([]), [])
        self.assertEqual(merge_sort([42]), [42])
        self.assertEqual(merge_sort([5, -3, 0, -3, 10]), [-3, -3, 0, 5, 10])

    def test_nu_modifica_lista_initiala(self) -> None:
        original = [9, 1, 5]
        _ = insertion_sort(original)
        _ = merge_sort(original)
        self.assertEqual(original, [9, 1, 5])

    def test_fara_sorted_sau_list_sort_in_cod(self) -> None:
        radacina = Path(__file__).resolve().parent.parent
        for nume_fisier in ("sortari.py", "main.py"):
            arbore = ast.parse((radacina / nume_fisier).read_text(encoding="utf-8"))
            for nod in ast.walk(arbore):
                if isinstance(nod, ast.Call):
                    if isinstance(nod.func, ast.Name):
                        self.assertNotEqual(nod.func.id, "sorted")
                    elif isinstance(nod.func, ast.Attribute):
                        self.assertNotEqual(nod.func.attr, "sort")


class TestRezolvaFisier(unittest.TestCase):
    """Teste pentru citire, validare si scriere in date.txt."""

    def test_exemplu_pdf_merge(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fisier = Path(tmpdir) / "date.txt"
            fisier.write_text("7 8 2 3 4 5\nMerge\n", encoding="utf-8")

            ok, mesaj = rezolva_fisier(fisier)
            self.assertTrue(ok)
            self.assertEqual(mesaj, "Merge: 2 3 4 5 7 8")
            self.assertEqual(
                fisier.read_text(encoding="utf-8"),
                "7 8 2 3 4 5\nMerge\nMerge: 2 3 4 5 7 8\n",
            )

    def test_rulare_exclusiva_un_singur_algoritm(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fisier = Path(tmpdir) / "date.txt"
            fisier.write_text("10 2 8\nInsertion\n", encoding="utf-8")

            with patch.dict(
                "main.ALGORITMI_DISPONIBILI",
                {
                    "insertion": ("Insertion", insertion_sort),
                    "merge": ("Merge", lambda _: self.fail("Merge nu trebuia apelat!")),
                },
            ):
                ok, mesaj = rezolva_fisier(fisier)
                self.assertTrue(ok)
                self.assertEqual(mesaj, "Insertion: 2 8 10")

    def test_rulare_consecutiva_si_normalizare_algoritm(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fisier = Path(tmpdir) / "date.txt"
            fisier.write_text(
                "7 8 2 3 4 5\n  insertion  \nMerge: 2 3 4 5 7 8\n",
                encoding="utf-8",
            )

            ok, mesaj = rezolva_fisier(fisier)
            self.assertTrue(ok)
            self.assertEqual(mesaj, "Insertion: 2 3 4 5 7 8")
            self.assertEqual(
                fisier.read_text(encoding="utf-8"),
                "7 8 2 3 4 5\n  insertion  \nInsertion: 2 3 4 5 7 8\n",
            )

    def test_fisier_inexistent(self) -> None:
        ok, mesaj = rezolva_fisier("/tmp/fisier_inexistent_lab6_test.txt")
        self.assertFalse(ok)
        self.assertIn("nu exista", mesaj)

    def test_fisier_incomplet_sub_doua_linii(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fisier = Path(tmpdir) / "date.txt"
            fisier.write_text("1 2 3\n", encoding="utf-8")
            ok, mesaj = rezolva_fisier(fisier)
            self.assertFalse(ok)
            self.assertIn("cel putin 2 linii", mesaj)

    def test_numere_invalide(self) -> None:
        with self.assertRaises(ValueError):
            parseaza_linie_numere("7 8 abc 5")
        with self.assertRaises(ValueError):
            parseaza_linie_numere("   ")

    def test_algoritm_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fisier = Path(tmpdir) / "date.txt"
            fisier.write_text("7 8 2\nQuick\n", encoding="utf-8")
            ok, mesaj = rezolva_fisier(fisier)
            self.assertFalse(ok)
            self.assertIn("nu este implementat", mesaj)


if __name__ == "__main__":
    unittest.main()
