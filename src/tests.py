import unittest
import fralgoparse

prog = '''Variables x, y, z en Numérique
Variable n en Entier
Variable s en Chaîne
Variable b en Booléen
Début
  x ← 1.2
  y ← 3.4
  z ← 5.6
  n ← 7
  s ← "Huit !"
  b ← VRAI
Fin'''

class Test(unittest.TestCase):
  def test(self):
    print(prog)
    print()

    fralgoparse.parser.parse(prog)

    x = fralgoparse.fralgoast.get_variable('x')
    y = fralgoparse.fralgoast.get_variable('y')
    z = fralgoparse.fralgoast.get_variable('z')
    n = fralgoparse.fralgoast.get_variable('n')
    s = fralgoparse.fralgoast.get_variable('s')
    b = fralgoparse.fralgoast.get_variable('b')

    self.assertEqual(x.value, 1.2, 'x should be 1.2')
    self.assertEqual(y.value, 3.4, 'y should be 3.4')
    self.assertEqual(z.value, 5.6, 'z should be 5.6')
    self.assertEqual(n.value, 7, 'n should be 7')
    self.assertEqual(s.value, 'Huit !', ' s should be Huit !')
    self.assertEqual(b.value, True, 'b should be VRAI')

    self.assertEqual(x.type, 'Numérique', 'x should be Numérique')
    self.assertEqual(y.type, 'Numérique', 'y should be Numérique')
    self.assertEqual(z.type, 'Numérique', 'z should be Numérique')
    self.assertEqual(n.type, 'Entier', 'n should be Entier')
    self.assertEqual(s.type, 'Chaîne', 's should be Chaîne')
    self.assertEqual(b.type, 'Booléen', 'b should be Booléen')

if __name__ == '__main__':
  unittest.main()
