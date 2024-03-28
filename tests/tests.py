import unittest
from algoparser import parser
from lib.datatypes import Array
import lib.symbols as sym

def reset_parser():
  try:
    parser.restart()
  except AttributeError:
    pass
  sym.reset_variables()

class Test(unittest.TestCase):

  def test_array_declaration(self):
    prog = '''Tableau T[] en Entier
    Début
      Ecrire "Test déclaration d'un tableau vide"
    Fin'''

    reset_parser()
    statements = parser.parse(prog)
    statements.eval()
    t = sym.get_variable('T')
    self.assertEqual(t.data_type, 'Tableau', 'should be Tableau')
    self.assertEqual(type(t), Array, 'should be Array')
    print()

  def test_multidimensional_array_declaration(self):
    prog = '''Tableau T[2, 2] en Entier
    Début
      Ecrire "Test déclaration d'un tableau multidimensionnel vide"
    Fin'''

    reset_parser()
    statements = parser.parse(prog)
    statements.eval()
    t = sym.get_variable('T')
    self.assertEqual(t.data_type, 'Tableau', 'should be Tableau')
    self.assertEqual(t.sizes, (3,3), 'should be (3,3)')
    self.assertEqual(type(t), Array, 'should be Array')
    print()

  def test_arrays_declaration(self):
    prog = '''Tableaux T1[], T2[2, 2], T3[3] en Entier
    Début
      Ecrire "Test déclarations de plusieurs tableaux"
    Fin'''

    reset_parser()
    statements = parser.parse(prog)
    statements.eval()
    t1 = sym.get_variable('T1')
    t2 = sym.get_variable('T2')
    t3 = sym.get_variable('T3')
    self.assertEqual(t1.data_type, 'Tableau', 'should be Tableau')
    self.assertEqual(t2.data_type, 'Tableau', 'should be Tableau')
    self.assertEqual(t3.data_type, 'Tableau', 'should be Tableau')
    self.assertEqual(t1.sizes, (0,), 'size should be 0')
    self.assertEqual(t2.sizes, (3,3), 'size should be 3,3')
    self.assertEqual(t3.sizes, (4,), 'size should be 4')
    print()

  def test_simple_array(self):
    prog = '''Tableau T[7] en Entier
    Variable I en Entier
    Début
      # Remplissage du tableau avec une boucle Pour
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
      Ecrire "Test de la boucle 'TantQue Marche'"
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
      Ecrire "Test de la boucle 'TantQue N < 11'"
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
      Ecrire "Test de la boucle 'Pour I <- 1 à 10'"
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
      Ecrire "Test de la boucle 'Pour I <- 10 à 0 Pas -1'"
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
      Ecrire "Test de la boucle 'Pour I <- 1 à 10 Pas 2'"
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
      Ecrire "Test de la boucle 'Pour I <- 0 à -10 Pas -2'"
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
      Ecrire "Test de la boucle 'Pour I <- 0 à -10'"
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
      Ecrire "Test de 'NON(A)'"
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
