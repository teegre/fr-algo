# FRALGO

## Types de données

### Booléen

`VRAI ou FAUX`

### Entier

`1`, `-6`, `33`

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

Exemple :

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

## Variables

### Déclaration

```
Variable a en Entier
Variables c1, c2, c3 en Chaîne
```

### Affectation

```
a <- 12
c1 <- "Chaîne1"
c2 <- "Chaîne2"
c3 <- c1 & " et " & c2
```

## Tableaux

### Déclaration

```
Tableau t1[4] en Entier
Tableaux u[], v[1,1], w[7,7,7] en Entier
```

### Affectation
```
t[0] <- 1
t[1] <- 2
t[2] <- 3
t[3] <- 4
v[0,0] <- 1
v[0,1] <- 2
...
w[0,0,0] <- 1
...
w[7,7,7] <- 512
```

### Dimensionnement

`Redim u[4]`

### Affectation d'un tableau à un autre tableau de même dimension :

```
u <- t
u = t
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
Variable p1, p2 en Personne
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
+
# Soustraction
-
# Multiplication
*
# Division
/
# Modulo
%
# Divisible par (renvoie VRAI si a est divisible par b)
DP
# Puissance
^
# Concaténation de chaînes de caractères
&
```

### Comparaisons

```
# Egal
=
# Différent
<>
# Supérieur
>
# Supérieur ou égal
>=
# Inférieur
<
# Inférieur ou égal
<=
```

### Opérateurs binaires

```
# Et
ET
# Ou
OU
# Ou exclusif
OUX
# Pas
NON(x)
# Si x est FAUX, NON(x) retourne VRAI et vice et versa.
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

## Fonctions prédéfinies

### Lire et Ecrire

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

### Manipulation de chaînes de caractères

```
# 'Longueur' renvoie la longueur d'une chaîne de caractères.
Longueur("ABC")
# 3
#
# 'Extraire' renvoie une sous-chaîne contenue dans une chaîne selon un
# index et une longueur donnés.
Extraire("Carte de crédit", 1, 5)
# Carte
#
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
#
# 10 'canaux' étant disponibles, il est possible d'ouvrir
# 10 fichiers simultanément.
#
# La fonction FDF retourne VRAI si la fin du fichier est atteinte sur
# le 'canal' spécifié en paramètre.
# Elle retourne FAUX dans le cas contraire.
#
# Modes d'ouverture :
# * Lecture permet de lire un fichier.
# * Ecriture permet d'écrire dans un fichier. Dans ce mode le contenu
# du fichier est préalablement effacé si le fichier existe, sinon le
# fichier est créé.
# * Ajout permet d'ajouter des lignes dans un fichier.
#
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
Taille(t)
# 8
```

## Fonctions

### Déclaration

```
Fonction somme(a, b en Entier) en Entier
  Retourne a + b
FinFonction
```

### Appel

```
somme(3, 4)
# 7
```

### Fonctions imbriquées

```
Fonction somme_mul(a, b en Entier) en Entier
  Fonction mul(a, b en Entier) en Entier
    Retourne 2 * (a * b)
  FinFonction
  Retourne mul(a, b)
FinFonction

somme_mul(4, 5)
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
