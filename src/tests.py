import unittest
import parse
import symbols

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

    parse.parser.parse(prog)

    x = symbols.get_variable('x')
    y = symbols.get_variable('y')
    z = symbols.get_variable('z')
    n = symbols.get_variable('n')
    s = symbols.get_variable('s')
    b = symbols.get_variable('b')

    self.assertEqual(x.data.value, 1.2, 'x should be 1.2')
    self.assertEqual(y.data.value, 3.4, 'y should be 3.4')
    self.assertEqual(z.data.value, 5.6, 'z should be 5.6')
    self.assertEqual(n.data.value, 7, 'n should be 7')
    self.assertEqual(s.data.value, 'Huit !', ' s should be Huit !')
    self.assertEqual(b.data.value, True, 'b should be VRAI')

    self.assertEqual(x.data.data_type, 'Numérique', 'x should be Numérique')
    self.assertEqual(y.data.data_type, 'Numérique', 'y should be Numérique')
    self.assertEqual(z.data.data_type, 'Numérique', 'z should be Numérique')
    self.assertEqual(n.data.data_type, 'Entier', 'n should be Entier')
    self.assertEqual(s.data.data_type, 'Chaîne', 's should be Chaîne')
    self.assertEqual(b.data.data_type, 'Booléen', 'b should be Booléen')

if __name__ == '__main__':
  unittest.main()
