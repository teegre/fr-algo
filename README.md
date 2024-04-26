# FR-ALGO

**FR-ALGO** (prononcé *F-R-ALGO*) est un interpréteur pour le pseudo-langage de programmation **ALGO**.

## Installation

Avant d'installer **FR-ALGO**, vérifiez que **python** version 3.10 ou plus,
**python-build** et **pipx** sont installés sur votre système :

```shell
$ python --version
Python 3.11.8
$ python -c "import build"
$ which pipx
/usr/bin/pipx
```
### Méthode 1

Cloner ce dépôt :
`$ git clone https://github.com/teegre/fr-algo`

Puis :
```
$ cd fr-algo
$ python -m build
$ pipx install dist/fralgo-0.11.2.tar.gz
```

### Méthode 2

```shell
$ wget https://github.com/teegre/fr-algo/releases/download/0.11.2/fr-algo_v0_11_2-beta_1.zip
$ unzip fr-algo_v0_11_2-beta_1.zip
$ pipx install fralgo-0.11.2.tar.gz
```

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
C'est un *environnement interactif* qui permet d'exécuter des expressions écrites en **ALGO**.

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
|A|L|G|O|R|I|T|H|M|E|S|                fr-v100 0.11.2mg

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
|A|L|G|O|R|I|T|H|M|E|S|                fr-v100 0.11.2mg

(c) 2024 Stéphane MEYER (Teegre)

Bonjour, Teegre !
En attente de vos instructions.

::: 1 + 1
--- 2
::: Ecrire "Bonjour le monde !"
Bonjour le monde !
```

Pour annuler une saisie en cours, appuyer sur <kbd>CTRL</kbd>+<kbd>c</kbd>.

Pour réinitialiser **l'environnement interactif**, taper `REINIT`.

Il est possible de naviguer dans l'historique avec les touches <kbd>↑</kbd> et <kbd>↓</kbd>
et d'effectuer une recherche avec <kbd>CTRL</kbd>+<kbd>r</kbd>.

Pour quitter, appuyer sur <kbd>CTRL</kbd>+<kbd>d</kbd>.

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

## Types de données

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
Attention, si l'on affecte une chaîne de longueur différente,
soit la valeur est tronquée, soit des espaces sont ajoutés à
la fin. En d'autres termes, une variable de type Caractère aura
toujours la même longueur, peu importe sa valeur.

Exemples :

```
Variable c en Caractère*5
c <- "ABC"
Longueur(c) = 5
# VRAI
# c = "ABC  "
c <- "ABCDEF"
Longueur(c) = 5
# VRAI
# c = "ABCDE"
```

```
Variable a en Caractère
a <- ""
Longueur(a)
# 1
a = ""
# FAUX
```

## Variables

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

## Tableaux

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

### Dimensionnement

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

## Structures

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

## Opérateurs

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

### Comparaisons

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

### Opérateurs binaires

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

## Lire et Ecrire

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

## Tests

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

### TantQue

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

### Pour

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

### Manipulation de chaînes de caractères

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

### Lecture / Ecriture de fichiers texte

```
# Lecture simple d'un fichier contenant les lignes suivantes :
# Ligne 1
# Ligne 2
# Ligne 3

Variable tampon en Chaîne
# Ouverture du ficher sur le 'canal' 1 en mode lecture.
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

### Conversion de types de données

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

### Tableaux

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

### Autres

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

# 'TempsUnix' retourne un "unix timestamp" de la date et l'heure courante.
# Exemple :
TempsUnix()
# 1714070687.823757
```

## Fonctions

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

## Procédures

### Déclaration

```
Procédure remplir(&t[] en Entier, taille en Entier)
  Variable i en Entier
  Si taille < 1 Alors
    Ecrire "Erreur : taille invalide ", taille, "]"
  Sinon
    Redim t[taille - 1]
    Pour i <- 0 à taille - 1
      t[i] <- Entier(Aléa() * 9 + 1)
    i Suivant
  FinSi
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

### Passage de variable par valeur ou par référence

Dans l'exemple précédent, le tableau `tab[]` est passé par référence (`&t[]`)
en paramètre de la procédure. C'est-à-dire que la variable ___globale___ `tab` est directement modifiée dans la procédure.

En ce qui concerne le paramètre `taille`, au contraire, seule la valeur de `n`, soit `8`
dans notre exemple, est passée. Une variable `taille` est d'abord créée ___localement___
lors de l'appel à la procédure `remplir`. Puis la valeur `8` est affectée à `taille`.
Enfin, la variable est détruite lorsque l'exécution de la procédure est terminée.

```
n = 8
# VRAI
```

## Importation de librairies ALGO

```
.
..
lib/
|__ ma_librairie.algo
|
|_ mon_projet.algo
```

```
# Ma librairie

Fonction ma_fonction(...) en ...
  ...
FinFonction

Procédure ma_procedure(...)
 ...
FinProcédure

# Mon projet
Importer "lib/ma_librairie"

Début
  ma_fonction(...)
  ma_procedure(...)
Fin

```
## Arguments de la ligne de commande

Une variable spéciale nommée `_ARGS` de type `Tableau` est disponible pour
gérer des arguments de la ligne de commande. Ses éléments sont tous du type
`Chaîne`

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
$ fralgo mon_programme "Bonjour tout le monde !"
Moi dire : Bonjour tout le monde !
```
Par défaut `_ARGS[0]` contient le nom du programme **ALGO** courant. Dans notre exemple,
`_ARGS[0]` est égal à `mon_programme.algo`.

## Programmes exécutables

Pour rendre un programe **ALGO** exécutable, il suffit d'abord d'y insérer la ligne
suivante en en-tête :

`#! /usr/bin/env fralgo`

Puis de changer les permissions du programme comme suit :
`chmod +x mon_programme.algo`

## Désinstallation

**Êtes-vous sûr de vouloir désinstaller FR-ALGO ?**

`$ pipx uninstall fralgo`
