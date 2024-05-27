import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import unittest
from fralgo.fralgoparse import parser
from fralgo.lib.ast import namespaces
from fralgo.lib.datatypes import Array
from fralgo.lib.symbols import Namespaces

sym = namespaces.get_namespace('main')

def reset_parser():
  try:
    parser.restart()
  except AttributeError:
    pass
  sym.reset()

class Test(unittest.TestCase):

  def test_table(self):
    prog='''Table t
      Clef en Entier
      Valeur en Entier
    FinTable
    Variables clef, valeur en Entier
    Variables test1, test2 en Booléen
    Début
      Ecrire "17. Test Table"
      clef <- Entier(Aléa() * 255 + 1)
      valeur <- Entier(Aléa() * 255 + 1)
      t[clef] <- valeur
      test1 <- t[clef] = valeur
      test2 <- NON(Existe(t, 0))
      Ecrire test1, test2
    Fin'''

    reset_parser()
    statements = parser.parse(prog)
    statements.eval()
    t1 = sym.get_variable('test1')
    t2 = sym.get_variable('test2')
    self.assertEqual(t1.eval(), True, 'test1 should be VRAI')
    self.assertEqual(t2.eval(), True, 'test2 should be VRAI')
    print()

  def test_procedure_split(self):
    prog = '''Procédure scinder(chaine, separateur, &elements[] en Chaîne)
     Variable sous_chaine en Chaîne
     Variable index en Entier
     index <- -1
     TantQue Trouve(chaine, separateur) > 0
       sous_chaine <- Gauche(chaine, Trouve(chaine, separateur) - 1)
       index <- index + 1
       Redim elements[index]
       elements[index] <- sous_chaine
       chaine <- Droite(chaine, Longueur(chaine) - Trouve(chaine, separateur))
     FinTantQue
     index <- index + 1
     Redim elements[index]
     elements[index] <- chaine
    FinProcédure
    Tableau tableau[] en Chaîne
    Variables test1, test2 en Booléen
    Début
      Ecrire "16. Test procédure et passage de variable par référence"
      scinder("TEST=REUSSI", "=", tableau)
      test1 <- tableau[0] = "TEST"
      test2 <- tableau[1] = "REUSSI"
      Ecrire test1, test2
    Fin'''

    reset_parser()
    statements = parser.parse(prog)
    statements.eval()
    t1 = sym.get_variable('test1')
    t2 = sym.get_variable('test2')
    self.assertEqual(t1.eval(), True, 'test1 should be VRAI')
    self.assertEqual(t2.eval(), True, 'test2 should be VRAI')
    print()

  def test_structure_in_resized_array(self):
    prog = '''Structure S
      a en Entier
      b en Entier
    FinStructure
    Tableau t[] en S
    Variables n, v en Entier
    Variables test1, test2 en Booléen
    Début
      Ecrire "15. Structure dans Tableau redimensionné"
      n <- -1
      Pour v <- 1 à 10 Pas 2
        n <- n + 1
        Redim t[n]
        t[n] <- v, v + 1
      v Suivant
      test1 <- t[0].a = 1 ET t[0].b = 2
      test2 <- t[n].a = 9 ET t[n].b = 10
      Ecrire test1, test2
    Fin'''

    reset_parser()
    statements = parser.parse(prog)
    statements.eval()
    t1 = sym.get_variable('test1')
    t2 = sym.get_variable('test2')
    self.assertEqual(t1.eval(), True, 'test1 should be VRAI')
    self.assertEqual(t2.eval(), True, 'test2 should be VRAI')
    print()

  def test_function(self):
    prog = '''Fonction somme_chaine(n1, n2 en Entier) en Chaîne
      # Retourne la somme de n1 et n2 en chaîne de caractères
      # sous la forme : "n1 + n2 = résultat"
      Retourne Chaîne(n1) & " + " & Chaîne(n2) & " = " & Chaîne(n1 + n2)
    FinFonction
    Variables x1, x2 en Entier
    Variables resultat, attendu en Chaîne
    Variable test en Booléen
    Début
      Ecrire "14. Test Fonction"
      x1 <- Entier(Aléa() * 10 + 1)
      x2 <- Entier(Aléa() * 10 + 1)
      resultat <- somme_chaine(x1, x2)
      attendu <- Chaîne(x1) & " + " & Chaîne(x2) & " = " & Chaîne(x1 + x2)
      test <- resultat = attendu
      Ecrire test
    Fin'''

    reset_parser()
    statements = parser.parse(prog)
    statements.eval()
    t = sym.get_variable('test')
    self.assertEqual(t.eval(), True, 'test should be VRAI')
    print()

  def test_structure(self):
    prog = '''Structure P
      a en Entier
      b en Entier
    FinStructure
    Variables p1, p2 en P
    Variables test1, test2, test3 en Booléen
    Début
      Ecrire "1. Test Structure"
      p1 <- 1, 2
      test1 ← p1.a = 1 ET p1.b = 2
      p1.a <- 3
      p1.b <- 4
      test2 ← p1.a = 3 ET p1.b = 4
      p2 <- p1
      test3 <- p2 = p1
      Ecrire test1, test2, test3
    Fin'''

    reset_parser()
    statements = parser.parse(prog)
    statements.eval()
    t1 = sym.get_variable('test1')
    self.assertEqual(t1.eval(), True, 'test1 should be VRAI')
    t2 = sym.get_variable('test2')
    self.assertEqual(t2.eval(), True, 'test2 should be VRAI')
    t3 = sym.get_variable('test3')
    self.assertEqual(t3.eval(), True, 'test3 should be VRAI')
    print()

  def test_array_declaration(self):
    prog = '''Tableau T[] en Entier
    Début
      Ecrire "2. Test déclaration d'un tableau vide"
    Fin'''

    reset_parser()
    statements = parser.parse(prog)
    statements.eval()
    t = sym.get_variable('T')
    self.assertEqual(t.data_type[0], 'Tableau', 'should be Tableau')
    self.assertEqual(type(t), Array, 'should be Array')
    print()

  def test_multidimensional_array_declaration(self):
    prog = '''Tableau T[2, 2] en Entier
    Début
      Ecrire "3. Test déclaration d'un tableau multidimensionnel vide"
    Fin'''

    reset_parser()
    statements = parser.parse(prog)
    statements.eval()
    t = sym.get_variable('T')
    self.assertEqual(t.data_type, ('Tableau', 'Entier', (2, 2)), 'should be Tableau')
    self.assertEqual(t.sizes, (3,3), 'should be (3,3)')
    self.assertEqual(type(t), Array, 'should be Array')
    print()

  def test_arrays_declaration(self):
    prog = '''Tableaux T1[], T2[2, 2], T3[3] en Entier
    Début
      Ecrire "4. Test déclarations de plusieurs tableaux"
    Fin'''

    reset_parser()
    statements = parser.parse(prog)
    statements.eval()
    t1 = sym.get_variable('T1')
    t2 = sym.get_variable('T2')
    t3 = sym.get_variable('T3')
    self.assertEqual(t1.data_type[0], 'Tableau', 'should be Tableau')
    self.assertEqual(t2.data_type[0], 'Tableau', 'should be Tableau')
    self.assertEqual(t3.data_type[0], 'Tableau', 'should be Tableau')
    self.assertEqual(t1.sizes, (0,), 'size should be 0')
    self.assertEqual(t2.sizes, (3,3), 'size should be 3,3')
    self.assertEqual(t3.sizes, (4,), 'size should be 4')
    print()

  def test_simple_array(self):
    prog = '''Tableau T[7] en Entier
    Variable I en Entier
    Début
      Ecrire "5. Remplissage du tableau avec une boucle Pour"
      Pour I ← 0 à 7
        T[I] ← I + 1
      I Suivant
      Si T[7] = 8 Alors
        Ecrire "T[7] est bien égal à 8 !"
      Sinon
        Ecrire "T[7] = 8 est", T[7] = 8
      FinSi
    Fin'''

    reset_parser()
    statements = parser.parse(prog)
    statements.eval()
    t = sym.get_variable('T')
    self.assertEqual(t.value[0], 1, 'Should be 1')
    self.assertEqual(t.value[1], 2, 'Should be 2')
    self.assertEqual(t.value[2], 3, 'Should be 3')
    self.assertEqual(t.value[3], 4, 'Should be 4')
    self.assertEqual(t.value[4], 5, 'Should be 5')
    self.assertEqual(t.value[5], 6, 'Should be 6')
    self.assertEqual(t.value[6], 7, 'Should be 7')
    self.assertEqual(t.value[7], 8, 'Should be 8')
    print()

  def test_while(self):
    prog = '''Variable Marche en Booléen
    Début
      Marche ← VRAI
      Ecrire "6. Test de la boucle 'TantQue Marche'"
      TantQue Marche
        Ecrire Marche
        Marche ← FAUX
      FinTantQue
      Ecrire Marche
    Fin'''

    reset_parser()
    statements = parser.parse(prog)
    statements.eval()
    m = sym.get_variable('Marche')
    self.assertEqual(m.eval(), False, 'should be False')
    print()

  def test_while_multable(self):
    prog = '''Variable N en Entier
    Début
      N ← 1
      Ecrire "7. Test de la boucle 'TantQue N < 11'"
      TantQue N < 11
        Ecrire N, "x 9 =", N * 9
        N ← N + 1
      FinTantQue
    Fin'''

    reset_parser()
    statements = parser.parse(prog)
    statements.eval()
    n = sym.get_variable('N')
    self.assertEqual(n.eval(), 11, 'should be 11')
    print()

  def test_for_loop_normal(self):
    prog = '''Variable I en Entier
    Début
      Ecrire "8. Test de la boucle 'Pour I <- 1 à 10'"
      Pour I ← 1 à 10
        Ecrire I
      I Suivant
    Fin'''

    reset_parser()
    statements = parser.parse(prog)
    statements.eval()
    i = sym.get_variable('I')
    self.assertEqual(i.eval(), 11, 'I should be 11')
    print()

  def test_for_loop_reverse(self):
    prog = '''Variable I en Entier
    Début
      Ecrire "9. Test de la boucle 'Pour I <- 10 à 0 Pas -1'"
      Pour I ← 10 à 0 Pas -1
        Ecrire I
      I Suivant
    Fin'''

    reset_parser()
    statements = parser.parse(prog)
    statements.eval()
    i = sym.get_variable('I')
    self.assertEqual(i.eval(), -1, 'I should be -1')
    print()

  def test_for_step_two(self):
    prog = '''Variable I en Entier
    Début
      Ecrire "10. Test de la boucle 'Pour I <- 1 à 10 Pas 2'"
      Pour I ← 1 à 10 Pas 2
        Ecrire I
      I Suivant
    Fin'''

    reset_parser()
    statements = parser.parse(prog)
    statements.eval()
    i = sym.get_variable('I')
    self.assertEqual(i.eval(), 11, 'I should be 11')
    print()

  def test_for_step_negative_two(self):
    prog = '''Variable I en Entier
    Début
      Ecrire "11. Test de la boucle 'Pour I <- 0 à -10 Pas -2'"
      Pour I ← 0 à -10 Pas -2
        Ecrire I
      I Suivant
    Fin'''

    reset_parser()
    statements = parser.parse(prog)
    statements.eval()
    i = sym.get_variable('I')
    self.assertEqual(i.eval(), -12, 'I should be -12')
    print()

  def test_for_negative(self):
    prog = '''Variable I en Entier
    Début
      Ecrire "12. Test de la boucle 'Pour I <- 0 à -10'"
      Pour I ← 0 à -10
        Ecrire I
      I Suivant
    Fin'''

    reset_parser()
    statements = parser.parse(prog)
    statements.eval()
    i = sym.get_variable('I')
    self.assertEqual(i.eval(), 0, 'I should be 0')
    print()

  def test_if_not(self):
    prog = '''Variables A, B en Booléen
    Début
      Ecrire "13. Test de 'NON(A)'"
      A ← VRAI
      Si NON(A) Alors
        B ← VRAI
      Sinon
        B ← FAUX
      FinSi
    Fin'''

    reset_parser()
    statements = parser.parse(prog)
    statements.eval()
    b = sym.get_variable('B')
    self.assertEqual(b.eval(), False, 'I should be False')
    print()

if __name__ == '__main__':
  unittest.main()
