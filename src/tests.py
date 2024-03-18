import unittest
import parser
import lib.symbols as sym

prog = '''# Commentaire
Variables x, y, z en Numérique
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
  Ecrire "Les valeurs de x, y et z sont " x ", " y ", " z
  Ecrire "n est égal à " n
  Ecrire "s vaut " s " et b est " b
Fin'''

class Test(unittest.TestCase):
  def test(self):
    print('Source :')
    print(prog)
    print()

    instructions = parser.parser.parse(prog)

    x = sym.get_variable('x')
    y = sym.get_variable('y')
    z = sym.get_variable('z')
    n = sym.get_variable('n')
    s = sym.get_variable('s')
    b = sym.get_variable('b')

    self.assertEqual(x.value, 1.2, 'x should be 1.2')
    self.assertEqual(y.value, 3.4, 'y should be 3.4')
    self.assertEqual(z.value, 5.6, 'z should be 5.6')
    self.assertEqual(n.value, 7, 'n should be 7')
    self.assertEqual(s.value, 'Huit !', ' s should be Huit !')
    self.assertEqual(b.value, True, 'b should be VRAI')

    self.assertEqual(x.data_type, 'Numérique', 'x should be Numérique')
    self.assertEqual(y.data_type, 'Numérique', 'y should be Numérique')
    self.assertEqual(z.data_type, 'Numérique', 'z should be Numérique')
    self.assertEqual(n.data_type, 'Entier', 'n should be Entier')
    self.assertEqual(s.data_type, 'Chaîne', 's should be Chaîne')
    self.assertEqual(b.data_type, 'Booléen', 'b should be Booléen')

    print('Instructions :')
    for instruction in instructions:
      print(instruction)
    print()

    print('Résultat :')
    instructions.eval()

if __name__ == '__main__':
  unittest.main()
