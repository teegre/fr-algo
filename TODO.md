# TODO

*  Ability to reset AST and symbols to perform more than a single big test. [OK]
*  Simple prompt with expected type for Lire [OK]
*  Debug: If `x = VRAI`, `Si NON(x)` is `VRAI` although `Ecrire NON(x)` returns `FAUX`. [FIXED]
*  Better AST representation.
*  Error code + detailed description.
*  Gauche("ABCD", 2) "AB", Droite("ABCD", 2) "CD"
*  Trouve("A B C D", "B C") 3, Trouve("ABC", "D") 0
*  Asc("A") 65, Chr(65) "A"
*  Ent("3.5") 3
*  Alea() returns a random number between 0 and 1
*  CNum("1") 1, CNum("1.5") 1.5, CCar(1) "1", CCar("1.5") 1.5
