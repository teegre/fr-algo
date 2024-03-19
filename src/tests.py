import unittest
from parser import parser
import lib.symbols as sym

prog = '''# Commentaire
Variables x, y, z, c en Numérique
Variable n en Entier
Variable s en Chaîne
Variable b en Booléen
Variable resultat en Entier
Début
  x ← 1.2
  y ← 3.4
  z ← 5.6
  n ← 7
  s ← "Huit !"
  b ← VRAI
  Ecrire "Les valeurs de x, y et z sont " x ", " y ", " z
  Ecrire "n est égal à " n
  Ecrire "s vaut " s " et b est " b
  resultat ← n + 8
  Ecrire "J'ai ajouté 8 à n et ça fait " resultat
  c ← x ^ 2
  Ecrire "J'ai mis x au carré : " c
  Ecrire "J'ai négationné le carré : " -c
  Ecrire "c est-il divisible par 2 ? " c dp 2
  Ecrire "c est-il divisible par 3 ? " c dp 3
  Ecrire "n est-il divisible par 7 ? " n dp 7
Fin'''

class Test(unittest.TestCase):
  def test(self):
    print('Source :')
    print(prog)
    print()

    parser.parse(prog)

    x = sym.get_variable('x')
    y = sym.get_variable('y')
    z = sym.get_variable('z')
    n = sym.get_variable('n')
    s = sym.get_variable('s')
    b = sym.get_variable('b')
    c = sym.get_variable('c')

    self.assertEqual(x.value, 1.2, 'x should be 1.2')
    self.assertEqual(y.value, 3.4, 'y should be 3.4')
    self.assertEqual(z.value, 5.6, 'z should be 5.6')
    self.assertEqual(n.value, 7, 'n should be 7')
    self.assertEqual(s.value, 'Huit !', ' s should be Huit !')
    self.assertEqual(b.value, True, 'b should be VRAI')
    self.assertEqual(c.value, 1.44, 'c should be 1.44')

    self.assertEqual(x.data_type, 'Numérique', 'x should be Numérique')
    self.assertEqual(y.data_type, 'Numérique', 'y should be Numérique')
    self.assertEqual(z.data_type, 'Numérique', 'z should be Numérique')
    self.assertEqual(n.data_type, 'Entier', 'n should be Entier')
    self.assertEqual(s.data_type, 'Chaîne', 's should be Chaîne')
    self.assertEqual(b.data_type, 'Booléen', 'b should be Booléen')
    self.assertEqual(c.data_type, 'Numérique', 'c should be Numérique')


if __name__ == '__main__':
  unittest.main()
