# FR-ALGO

**FR-ALGO** (prononcé *F-R-ALGO*) est un interpréteur pour le pseudo-langage de programmation **ALGO**.

## Installation

Avant d'installer **FR-ALGO**, vérifiez que **python** version 3.10 (ou ultérieure) et **pipx** sont installés sur votre système :

```shell
$ python --version
Python 3.11.8
$ which pipx
/usr/bin/pipx
```

Cloner ce dépôt :

`git clone https://github.com/teegre/fr-algo`

Puis :

```
$ cd fr-algo
$ python -m build
```

Et installer **FR-ALGO** à l'aide de la commande suivante :

```
$ pipx install dist/fralgo-0.11.2b7.tar.gz
```

**/!\ Le numéro de version peut être différent.**

## Utilisation

### fralgo

Ce programme en ligne de commande permet d'exécuter un programme écrit en **ALGO** préalablement enregistré dans un fichier.

`fralgo <fichier>`

où `<fichier>` est un fichier contenant un programme écrit en **ALGO**.

#### Exemple

```
Début
  Ecrire "Bonjour le monde !"
Fin
```

Pour exécuter le programme ci-dessus enregistré dans le fichier `bonjour.algo`, il suffit d'entrer cette commande dans un terminal :

`$ fralgo bonjour.algo`

Après un appui sur la touche <kbd>Entrée</kbd>, nous obtenons :

```
$ fralgo bonjour.algo
Bonjour le monde !
$
```

### fralgorepl

Ce programme est un **REPL** (**R**ead-**E**val-**P**rint-**L**oop), en français : **boucle de lecture, d'évaluation et d'affichage**.
C'est un **environnement interactif** qui permet d'exécuter des expressions écrites en **ALGO**.

Pour charger **l'environnement interactif**, entrer la commande suivante :

```
$ fralgorepl
```

Une invite de commande est alors affichée...

```
$ fralgorepl
 _______ ______        _______ _____   _______ _______
|    ___|   __ \______|   _   |     |_|     __|       |
|    ___|      <______|       |       |    |  |   -   |
|___|   |___|__|      |___|___|_______|_______|_______|
|A|L|G|O|R|I|T|H|M|E|S|         fr-v100 0.11.2.beta.6mg

(c) 2024 Stéphane MEYER (Teegre)

Bonjour, Teegre !
En attente de vos instructions.

:::
```

... Et l'on peut entrer n'importe quelle expression en **ALGO** qui sera exécutée après un appui sur la touche <kbd>Entrée</kbd>

```
$ fralgorepl
 _______ ______        _______ _____   _______ _______
|    ___|   __ \______|   _   |     |_|     __|       |
|    ___|      <______|       |       |    |  |   -   |
|___|   |___|__|      |___|___|_______|_______|_______|
|A|L|G|O|R|I|T|H|M|E|S|         fr-v100 0.11.2.beta.6mg

(c) 2024 Stéphane MEYER (Teegre)

Bonjour, Teegre !
En attente de vos instructions.

::: 1 + 1
--- 2
::: Ecrire "Bonjour le monde !"
Bonjour le monde !
```

Pour annuler une saisie en cours, appuyer sur <kbd>CTRL</kbd>+<kbd>c</kbd>.

Pour réinitialiser **l'environnement interactif**, taper `.réinit`.

Il est possible de naviguer dans l'historique avec les touches <kbd>↑</kbd> et <kbd>↓</kbd> et d'effectuer une recherche avec <kbd>CTRL</kbd>+<kbd>r</kbd>.

Pour quitter, appuyer sur <kbd>CTRL</kbd>+<kbd>d</kbd>.

## Commandes

Outre la commande `.réinit` citée plus haut, il existe d'autres commandes qui permettent d'obtenir des informations sur l'environnement en cours :

*  `.espaces` - affiche la liste des espaces en cours
*  `.symboles [espace]` - fournit des informations sur l'espace donné (constantes, variables, structures, procédures et fonctions)

## Syntaxe

Elle doit être scrupuleusement appliquée sous peine d'avoir des erreurs lors de l'exécution des programmes !

Les <u>mots reservés</u> sont <u>sensibles à la casse</u> et aux <u>accents</u>, par exemple :

`Debut`, `debut`, `Début` seront traîtés différemment par l'interpréteur.
En effet, si `Début` est un mot reservé indiquant le commencement d'un programme **ALGO**, `Debut` et `debut` sont considérés comme des <u>variables</u>.

Il est à noter que **chaque instruction d'un programme ALGO**, **doit être suivie d'un retour à la ligne** et les éventuels sauts
de ligne après le mot réservé `Fin` provoquent une erreur de syntaxe.

### Commentaires

Il est possible d'ajouter des commentaires comme suit :

```
# Ceci est commentaire.
Variable c en Chaîne
# Ceci est un autre commentaire.
Début
  # Encore un commentaire.
  Ecrire "Bonjour le monde !"
Fin
```

**Les commentaires en fin de ligne ne sont pas acceptés.**

## Types de données  <a name="type"></a>

### Booléen

`VRAI ou FAUX`

### Entier

`1`, `-2`, `3`

### Numérique

`1.2`, `-3.4`, `5.67`

### Chaîne

`"Bonjour"`

### Caractère

`"A"`

On peut spécifier une longueur comme suit : `Caractère*10`

Attention, si l'on affecte une chaîne de longueur différente, soit la valeur est tronquée, soit des espaces sont ajoutés à la fin.

En d'autres termes, une variable de type Caractère aura toujours la même longueur, peu importe sa valeur.

Exemples :

```
Variable c en Caractère*5
c <- "ABC"
Longueur(c) = 5
# VRAI
c = "ABC  "
# VRAI
c <- "ABCDEF"
c = "ABCDEF"
# FAUX
c = "ABCDE"
# VRAI
Longueur(c) = 5
# VRAI
```

```
Variable a en Caractère
a <- ""
Longueur(a)
# 1
a = ""
# FAUX
```

## Variables <a name="variable"></a>

### Déclaration

```
Variable a en Entier
Variables c1, c2, c3 en Chaîne
```

### Affectation

```
a <- (12 * 2 / 4) + 1
c1 <- "Chaîne1"
c2 <- "Chaîne2"
c3 <- c1 & " et " & c2
a = 7
# VRAI
c3 = "Chaîne1 et Chaîne2"
# VRAI
```

**Note** : Si une valeur de type `Entier` est affectée à une variable de type `Numérique`,
elle est convertie en `Numérique`.

```
Variable n en Numérique
n <- 1
n
# 1.0
```

## Constantes

### Déclaration

`Constante C 12`

## Affectation

La valeur d'un constante ne peut évidemment pas être modifiée.

```
C ← 13
*** Constante C : en lecture seule
```

Il est possible d'affecter à une constante les types suivants :

`Chaîne`, `Entier`, `Numérique`, `Booléen`, `Tableau`

L'affectation d'un tableau à une constante se fait de la manière suivante :
`Constante MonTableau [1, 2, 3]`

## Tableaux <a name="tableau"></a>

### Déclaration

```
Tableau t1[3] en Entier
# t1[3] désigne un tableau pouvant contenir 4 éléments (numérotés de 0 à 3).

Tableau u[]
# u[] désigne un tableau qui sera dimensionné ultérieurement (voir plus bas).

Tableaux v[1,1], w[7,7,7] en Entier
```

### Affectation

```
t[0] <- 1
t[1] <- 2
t[2] <- 3
t[3] <- 4
v[0,0] <- 1
v[0,1] <- 2
v[1,0] <- 3
v[1,1] <- 4
...
w[0,0,0] <- 1
...
w[7,7,7] <- 512
```

### Dimensionnement <a name="redim"></a>

`Redim u[3]`

### Affectation d'un tableau à un autre tableau de même dimension :

```
u <- t
u = t
# VRAI
u[3] = t[3]
# VRAI
u[3] = 4
# VRAI
```

### Affectation d'une liste de valeurs à un tableau

```
Tableau T[3] en Entier
T <- 1, 2, 3, 4
# ou
T <- [1, 2, 3, 4]
T[0] = 1
# VRAI
T[3] = 4
# VRAI
```

Il est également possible d'affecter une liste de tableaux à un tableau.
Pour cela la somme des tailles des tableaux à affecter doit être égale à la taille de la cible. Exemple :

```
Tableaux T[9], A[4], B[4] en Entier
A <- 1, 2, 3, 4, 5
B <- 6, 7, 8, 9, 10
Taille(T)
# 10
Taille(A)
# 5
Taille(B)
# 5

T <- A, B
T
# [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

## Tables <a name="table"></a>

Une `Table` est un **tableau associatif**.

Plutôt que d'utiliser des **index** comme dans un `Tableau`, le type `Table` utilise des **clefs** qui seront associées à des **valeurs**.

### Déclaration

```
Table t
  Clef en Chaîne
  Valeur en Entier
FinTable
```

### Affectation

```
t["A"] <- 65
t["B"] <- 66
t["A"] = 65
# VRAI
```

## Structures <a name="structure"></a>

### Déclaration

```
Structure Personne
  prenom en Chaîne
  nom en Chaîne
FinStructure

# Déclaration d'une variable de type Personne
Variables p1, p2 en Personne
```

### Affectation

```
p1.prenom <- "John"
p1.nom <- "Wick"
# ou
p1 <- "John", "Wick"
# aussi
p2 <- p1
p2 = p1
# VRAI
```

### Accès aux champs d'une structure

Pour récupérer la valeur d'un champ, la syntaxe est la suivante :

```
p1.prenom
# John
p1.nom
# Wick
```

## Opérateurs <a name="opérateur"></a>

### Opérations

```
# Addition
a + b

# Soustraction
a - b

# Multiplication
a * b

# Division
a / b
# Note : si a et b sont de type Entier, le quotient sera également de type Entier.

# Modulo (reste de la division)
a % b

# Divisible par (retourne VRAI si a est divisible par b)
a DP b

# Puissance
a ^ b

# Concaténation de chaînes de caractères
a & b
```

### Comparaisons <a name="comparaison"></a>

```
# Egal
a = b

# Différent
a <> b

# Supérieur
 a > b

# Supérieur ou égal
a >= b

# Inférieur
a < b

# Inférieur ou égal
a <= b
```

### Opérateurs binaires <a name="opérateur_binaire"></a>

```
# Et
a ET b

# Ou
a OU b

# Ou exclusif
a OUX b

# Pas
NON(x)
# Si x est FAUX, NON(x) retourne VRAI et vice et versa.
```

## Lire et Ecrire <a name="lire"></a>

```
Variable n en Entier
Lire n
# Affecte la valeur entrée par l'utilisateur à la variable 'n'.

Ecrire n
# Affiche la valeur de n.

Ecrire n, x
# Affiche les valeurs de n et de x séparées par un espace.
# Par exemple :
# 74 19

Ecrire n
Ecrire x
# 74
# 19

Ecrire n \
Ecrire x
# 7419
# Le caractère '\' indique à la fonction Ecrire de ne pas 
# passer à la ligne suivante, et lors du second appel à
# Ecrire, la valeur de x est affichée directement après 
# celle de n.
#
# Application :
Ecrire "Entrer un nombre : " \
Lire n
# Entrer un nombre : _
# _ indique la position du curseur.
#
# Note :
# La fonction Lire essayera de convertir la valeur d'entrée (toujours
# de type Chaîne) en le type attendu par la variable donnée en paramètre.
# Par exemple :
Variable n en Entier
Lire n
# Valeur entrée par l'utilisateur = 12
n = 12
# VRAI
# Si la conversion de type échoue, une erreur est générée :
Lire n
# Valeur entrée par l'utilisateur = 12.34
*** Type Entier attendu
```

## Tests <a name="test"></a>

```
Variable temperature en Entier
Ecrire "Température de l'eau ?"
Lire temperature
Si temperature <= 0 Alors
  Ecrire "C'est de la glace"
SinonSi temperature < 100 Alors
  Ecrire "C'est de l'eau"
Sinon
  Ecrire "C'est de la vapeur"
FinSi
```

## Boucles

### TantQue <a name="tant"></a>

```
Variable i en Entier
i <- 1

TantQue i < 6
  Ecrire i
  i <- i + 1
FinTantQue
# 1
# 2
# 3
# 4
# 5
```

### Pour <a name="pour"></a>

```
Variable i en Entier

Pour i <- 1 à 5
  Ecrire i
i Suivant
# 1
# 2
# 3
# 4
# 5

Pour i <- 1 à 10 Pas 2
  Ecrire i
i Suivant
# 1
# 3
# 5
# 7
# 9

Pour i <- 10 à 1 Pas -2
  Ecrire i
i Suivant
# 10
# 8
# 6
# 4
# 2
```

## Fonctions prédéfinies

### Manipulation de chaînes de caractères <a name="chaîne"></a>

```
# 'Longueur' renvoie la longueur d'une chaîne de caractères.
Longueur("ABC")
# 3

# 'Extraire' renvoie une sous-chaîne contenue dans une chaîne selon un
# index et une longueur donnés.
Extraire("Carte de crédit", 1, 5)
# Carte

# 'Gauche' renvoie la sous-chaîne d'une longueur donnée à partir du
# début d'une chaîne.
Gauche("Carte de crédit", 5)
# Carte

# 'Droite' renvoie la sous-chaîne d'une longueur donnée à partir de
# la fin d'une chaîne.
Droite("Carte de crédit", 6)
# crédit

# 'Trouve' renvoie l'index d'une sous-chaîne dans une chaîne.
Trouve("Carte de crédit", "crédit")
# 10

# 'CodeCar' retourne le code ASCII du caractère donné en paramètre :
CodeCar("A")
# 65

# Car retourne le caractère correspondant au code ASCII donné en paramètre :
Car(65)
# A
```

### Lecture / Ecriture de fichiers texte <a name="fichier"></a>

```
# Lecture simple d'un fichier contenant les lignes suivantes :
# Ligne 1
# Ligne 2
# Ligne 3

Variable tampon en Chaîne
# Ouverture du fichier sur le 'canal' 1 en mode lecture.
Ouvrir "fichier.txt" sur 1 en Lecture
# Tant que la fin du fichier (FDF(1)) n'est pas atteinte...
TantQue NON(FDF(1))
  # ... on lit une ligne dans le fichier ouvert sur le 'canal' 1
  # que l'on affecte à la variable 'tampon' de type Chaîne.
  LireFichier 1, tampon
  # On affiche la ligne lue à l'écran.
  Ecrire tampon
FinTantQue
# Fermeture du fichier ouvert sur le 'canal' 1
Fermer 1

# 10 'canaux' étant disponibles, il est possible d'ouvrir
# 10 fichiers simultanément.
#
# La fonction FDF retourne VRAI si la fin du fichier est atteinte sur
# le 'canal' spécifié en paramètre.
# Elle retourne FAUX dans le cas contraire.

# Modes d'ouverture :
# * Lecture permet de lire un fichier.
# * Ecriture permet d'écrire dans un fichier. Dans ce mode le contenu
# du fichier est préalablement effacé si le fichier existe, sinon le
# fichier est créé.
# * Ajout permet d'ajouter des lignes dans un fichier.

# Pour écrire dans un fichier, on utilise la fonction 'EcrireFichier'
# Exemple :
Variable i en Entier
Ouvrir "fichier.txt" sur 2 en Ecriture
Pour i <- 1 à 3
  EcrireFichier 2, "Ligne " & Chaîne(i)
i Suivant
Fermer 2

# De même en mode Ajout :
Ouvrir "fichier.txt" sur 1 en Ajout
EcrireFichier 1, "Ligne 4"
Fermer 1
```

### Conversion de types de données <a name="conversion"></a>

```
Chaîne(123)
# "123"

Chaîne(1.23)
# "1.23"

Entier("123")
# 123

Entier(1.23)
# 1

Numérique("1.23")
# 1.23

Numérique(1)
# 1.0
```

### Obtenir le type de données <a name="type"></a>

La fonction `Type` retourne une `Chaîne` décrivant le type d'une variable ou d'une expression.

```
Type(1)
# Entier

Type(1.23)
# Numérique

Type("Bonjour")
# Chaîne

Tableau T[] en Entier
Type(T)
# Tableau[] en Entier

Redim T[5]
Type(T)
# Tableau[5] en Entier

...
```

### Tableaux <a name="fonction_tableau"></a>

```
Tableau t[7] en Entier
# 'Taille' retourne la taille du tableau donné en paramètre.
Taille(t)
# 8

# Dans le cas d'un tableau multidimensionnel, 'Taille' retourne
# un tableau contenant les tailles de chaque sous-tableau.
Tableau t2[7,7]
Taille(t2)
# [8, 8]
```

### Tables <a name="fonctions_table"></a>

```
Table t
  Clef en Chaîne
  Valeur en Entier
FinTable

Variable idx en Entier

Pour i <- 65 à 90
  t[Car(idx)] <- idx
i Suivant

# 'Longueur' ou 'Taille' retourne le nombre d'éléments dans une table.
Longueur(t)
# 26
Taille(t)
# 26

# 'Existe' retourne VRAI si une clef existe dans une table donnée.
Existe(t, "A")
# VRAI
Existe(t, "0")
# FAUX

# 'Clefs' retourne la liste des clefs.
Clefs(t)
# ["A", "B", "C", ..., "X", "Y", "Z"]

# 'Valeurs' retourne la liste de valeurs.
Valeurs(t)
# [65, 66, 67, ..., 88, 89, 90]
```

### Autres <a name="autre"></a>

```
# 'Aléa' retourne un `Numérique` entre 0 et 1.
# Exemple :
# Aléa()
# 0.54575648

# 'Dormir' suspend l'exécution du programme pendant une durée en
# secondes donnée en paramètre.
# La durée peut être de type Entier ou Numérique.
# Exemples :
Dormir(1)
Dormir(0.5)

# 'Panique' interrompt le programme en cours d'exécution
# Exemple :
Fonction PlusUn(n en Quelconque) en Quelconque
  Si Type(n) <> "Entier" OU Type(n) <> "Numérique" Alors
    Panique "Je ne peux pas ajouter 1 à", n
  FinSi
  Retourne n + 1
FinFonction

# 'TempsUnix' retourne un "unix timestamp" de la date et l'heure courante.
# Exemple :
TempsUnix()
# 1714070687.823757
```

## Fonctions <a name="fonction"></a>

### Déclaration

```
Fonction somme(a, b en Entier) en Entier
  Retourne a + b
FinFonction
```

Note : une fonction doit nécessairement retourner une valeur.

### Appel

```
somme(3, 4)
# 7
```

### Fonctions imbriquées

```
Fonction double_produit(a, b en Entier) en Entier
  # Double la produit de a et b
  Fonction mul(a, b en Entier) en Entier
    Retourne a * b
  FinFonction
  Retourne 2 * mul(a, b)
FinFonction

double_produit(4, 5)
# 40
```

### Fonctions récursives

```
Fonction factorielle(n en Entier) en Entier
  Si n = 0 Alors
    Retourne 1
  FinSi
  Retourne factorielle(n - 1) * n
FinFonction

factorielle(10)
# 3628800
```

## Procédures <a name="procédure"></a>

### Déclaration

```
Procédure remplir(&t[] en Entier, taille en Entier)
  # Redimensionne un tableau selon une taille donnée et
  # le remplit avec des valeurs aléatoires comprises
  # entre 1 et 9.
  Variable i en Entier
  Si taille < 1 Alors
    Ecrire "Erreur : taille invalide [", taille, "]"
  Sinon
    Redim t[taille - 1]
    Pour i <- 0 à taille - 1
      t[i] <- Entier(Aléa() * 9 + 1)
    i Suivant
  FinSi
FinProcédure
```

Note : une procédure ne retourne <u>jamais</u> de valeur.

Il est possible d'interrompre l'exécution d'une procédure
avec l'instruction `Terminer`.

Reprenons l'exemple précédent :

```
Procédure remplir(&t[] en Entier, taille en Entier)
  Variable i en Entier
  Si taille < 1 Alors
    Ecrire "Erreur : taille invalide [", taille, "]"
    Terminer
  FinSi
  Redim t[taille - 1]
  Pour i <- 0 à taille - 1
    t[i] <- Entier(Aléa() * 9 + 1)
  i Suivant
FinProcédure
```

### Appel

```
Tableau tab[] en Entier
Variable n en Entier
n <- 8
remplir(tab, n)
# Exemple de résultat :
# t = [1, 2, 8, 6, 8, 5, 7, 3]
```

## Passage de variable par valeur ou par référence

Dans l'exemple précédent, le tableau `tab[]` est passé par référence (`&t[]`)en paramètre de la procédure. C'est-à-dire que la variable ___globale___ `tab` est directement modifiée dans la procédure.

En ce qui concerne le paramètre `taille`, au contraire, seule la valeur de `n`, soit `8` dans notre exemple, est passée. Lors de l'appel à la procédure `remplir`, une variable `taille` est créée ___localement___ et la valeur `8` est affectée à `taille`.
Enfin, la variable est détruite lorsque l'exécution de la procédure est terminée, laissant intacte la variable originale `n`.

```
n = 8
# VRAI
```

Autre exemple :

```
Variables y, z en Entier

Procédure test_ref_val(&ref en Entier, val en Entier)
  Ecrire "Avant : valeur de ref =", ref, ", valeur de val =", val
  ref <- 123
  val <- 456
  Ecrire "Après : valeur de ref =", ref, ", valeur de val = ", val
FinProcédure

y <- 1999
z <- 777

test_ref_val(y, z)
# Avant : valeur de ref = 1999, valeur de val = 777
# Après : valeur de ref = 123, valeur de val = 456

y
# La valeur de y a changé :
# 123

z
# Mais pas celle de z :
# 177
```

## Le type `Quelconque` <a name="quelconque"></a>

C'est un type générique qui peut être n'importe lequel des types suivants :
`Booléen`, `Entier`, `Numérique` ou `Chaîne`.
Il est utilisable dans les paramètres et/ou dans le corps d'une fonction ou d'une procédure.
Il peut être également utilisé comme type retourné par une fonction.

### Utilité

Un exemple : vous devez écrire une fonction qui retourne le nombre d'occurences d'un élément dans un tableau.
Un tableau ne pouvant contenir qu'un seul type d'éléments, il est nécessaire d'écrire une fonction par type :

```
Fonction CompteEntier(T[] en Entier, valeur en Entier) en Entier
  Variables i, c en Entier
  c <- 0
  Pour i <- 0 à Taille(T) - 1
    Si T[i] = valeur Alors
      c <- c + 1
    FinSi
  i Suivant
  Retourne c
FinFonction

Fonction CompteNumérique(T[] en Numérique, valeur en Numérique) en Entier
  # Corps de la fonction identique au précédent...
  # ...
FinFonction

Fonction CompteChaîne(T[] en Chaîne, valeur en Chaîne) en Entier
  # Corps de la fonction identique à CompteEntier()...
  # ...
FinFonction

# ...
```

Pour éviter cette ennuyeuse redondance, il est possible d'utiliser le type `Quelconque` :

```
Fonction Compte(T[] en Quelconque, valeur en Quelconque) en Entier
  Variables i, c en Entier
  c <- 0
  Pour i <- 0 à Taille(T) - 1
    Si T[i] = valeur Alors
      c <- c + 1
    FinSi
  i Suivant
  Retourne c
FinFonction
```

De cette manière, une seule fonction est nécessaire pour tous les types
cités précédemment.

Au besoin, il existe une fonction `Type` qui permet d'obtenir le type d'une variable
ou d'une expression.

```
Fonction Compte(T[] en Quelconque, valeur en Quelconque) en Entier
  Variables i, c en Entier
  c <- 0
  # On affiche le type de 'T' et de 'valeur'
  Ecrire "T :", Type(T), "; valeur :", Type(valeur)
  Pour i <- 0 à Taille(T) - 1
    Si T[i] = valeur Alors
      c <- c + 1
    FinSi
  i Suivant
  Retourne c
FinFonction

Tableau T1[4] en Chaîne
Tableau T2[4] en Entier

Début
  T1[] <- "A", "B", "C", "D", "A"
  T2[] <- 1, 2, 1, 3, 1
  Ecrire "T1 contient", Compte(T1, "A"), "fois la lettre A."
  Ecrire "T2 contient", Compte(T2, 1), "fois le chiffre 1."
Fin
```

A l'exécution du programme ci-dessus, on obtient :

```
T : Tableau[4] en Chaîne ; valeur : Chaîne
T1 contient 2 fois la lettre A.
T : Tableau[4] en Entier ; valeur : Entier
T2 contient 3 fois le chiffre 1.
```

## Structure d'un programme ALGO <a name="programme"></a>

### Minimum

* `Début`
* Instructions
* `Fin`

### Maximum

* Déclaration de variables, de constantes de tableaux, de structures...
* Déclaration de fonctions, de procédures...
* `Début`
* Instructions
* `Fin`

## Librairies et importation de librairies ALGO <a name="librairie"></a>

Une **librairie** est un fichier qui peut contenir des variables, des structures, des tableaux, des fonctions et des procédures qui pourront être réutilisées dans d'autres programmes **ALGO**.

La structure d'une librairie se présente comme suit :



* `Librairie`
* Déclarations
  
  

Au besoin, si des variables doivent être initialisées ou si des ajustements sont nécessaires (comme par exemple remplir un tableau, appeler une fonction, etc.), on utilise le mot réservé `Initialise` :



* `Librairie`
* Déclarations
* `Initialise`
* Instructions

### Exemple de librairie et importation dans un programme

```
.
..
lib/
|__ librairie.algo
|
|_ projet.algo
|_ utilitaires.algo
```

```
# Ma librairie
Librairie

Variable ma_variable en Chaîne

Fonction ma_fonction(...) en ...
  ...
FinFonction

Procédure ma_procedure(...)
 ...
FinProcédure

Initialise
  ma_variable <- "Bonjour"

# Utilitaires
Librairie

Fonction date() en Chaîne
  ...
FinFonction

Fonction heure() en Chaîne
  ...
FinFonction

# Mon projet
# La fonction 'Importer' permet d'inclure une librairie
Importer "lib/librairie"

Début
  # On accède aux membres d'une librairie de la manière suivante :
  librairie:ma_fonction(...)
  librairie:ma_procedure(...)
  Ecrire librairie:ma_variable
Fin

# Il est également possible de définir un 'alias' pour une librairie :
Importer "utilitaires" Alias utils

Début
  Ecrire utils:date(), utils:heure()
Fin

# Note : Lors de l'importation d'une librairie, fr-algo vérifie si elle
# existe dans le répertoire où se trouve le programme principal.
# Si ce n'est pas le cas, le répertoire '$HOME/.local/lib/fralgo' est
# utilisé.
# L'importation d'une librairie se fait de manière globale. C'est à dire
# que celle-ci sera disponible dans le programme principal ainsi que dans
# toutes les autres librairies importées.
```

### Eléments privés

Il est parfois souhaitable que l'accès à une fonction, une procédure une variable ou une constante soit limité à la librairie à laquelle elle appartient.

Pour ce faire il suffit de faire débuter le nom de l'élément par `___` (3 tirets de soulignement).

## Arguments de la ligne de commande <a name="argument"></a>

Une variable spéciale nommée `_ARGS` de type `Tableau` est disponible pour gérer des arguments de la ligne de commande. Ses éléments sont tous du type `Chaîne`

Exemple :

```
# mon_programme.algo
Procédure repete(phrase en Chaîne, nombre en Entier)
  TantQue nombre > 0
    Ecrire phrase
    nombre <- nombre - 1
  FinTantQue
FinProcédure

Début
  repete(_ARGS[1], Entier(_ARGS[2]))
Fin
```

```shell
$ fralgo mon_programme.algo "Bonjour tout le monde !" 2
Bonjour tout le monde !
Bonjour tout le monde !
```

Par défaut `_ARGS[0]` contient le nom du programme **ALGO** courant. Dans notre exemple,
`_ARGS[0]` est égal à `mon_programme.algo`.

## Chemin vers le programme courant <a name="répertoire"></a>

La variable `_REP` contient le chemin vers le programme courant.

## Programmes exécutables

Pour rendre un programe **ALGO** exécutable, il suffit d'abord d'y insérer la ligne
suivante en en-tête :

`#! /usr/bin/env fralgo`

Puis de changer les permissions du programme comme suit :
`chmod +x mon_programme.algo`

## Désinstallation

**Êtes-vous sûr de vouloir désinstaller FR-ALGO ?**

`$ pipx uninstall fralgo`

## Index des mots reservés et fonctions prédéfinies

### -

[%](#opérateur)

[&](#opérateur)

[*](#opérateur)

[+](#opérateur)

[-](#opérateur)

[/](#opérateur)

[^](#opérateur)

[_ARGS](#argument)

[_REP](#répertoire)

### A

[à](#pour)

[Ajout](#fichier)

[Alias](#librairie)

[Alors](#test)

[Aléa](#autre)

### B

[Booléen](#type)

### C

[Car](#chaîne)

[Caractère](#type)

[Chaîne](#type)

[Chaîne()](#conversion)

[Clefs](#fonctions_table)

[CodeCar](#chaîne)

### D

[DP](#opérateur)

[Dormir](#autre)

[Droite](#chaîne)

[Début](#programme)

### E

[en](#variable)

[en (mode d'ouverture)](#fichier)

[ET](#opérateur_binaire)

[Ecrire](#lire)

[EcrireFichier](#fichier)

[Ecriture](#fichier)

[Entier](#type)

[Entier()](#conversion)

[Existe](#fonctions_table)

[Extraire](#chaîne)

### F

[FDF](#fichier)

[Fermer](#fichier)

[Fin](#programme)

[FinProcédure](#procédure)

[FinSi](#test)

[FinStructure](#structure)

[FinTantQue](#tant)

[Fonction](#fonction)

### G

[Gauche](#chaîne)

### I

[Importer](#librairie)

[Initialise](#librairie)

### L

[Lecture](#fichier)

[Librairie](#librairie)

[Lire](#lire)

[LireFichier](#fichier)

[Longueur](#chaîne)

### N

[NON](#opérateur_binaire)

[Numérique](#type)

[Numérique()](#conversion)

### O

[OU](#opérateur_binaire)

[OUX](#opérateur_binaire)

[Ouvrir](#fichier)

### P

[Panique](#autre)

[Pas](#pour)

[Pour](#pour)

[Procédure](#procédure)

### Q

[Quelconque](#quelconque)

### R

[Redim](#redim)

[Retourne](#fonction)

### S

[Si](#test)

[Sinon](#test)

[SinonSi](#test)

[Structure](#structure)

[Suivant](#pour)

[sur](#fichier)

### T

[Table](#table)

[Tableau](#tableau)

[Tableaux](#tableau)

[Taille](#fonction_tableau)

[TempsUnix](#autre)

[Terminer](#procédure)

[Trouve](#chaîne)

[Type](#type)

### V

[Valeurs](#fonctions_table)

[Variable](#variable)

[Variables](#variable)
