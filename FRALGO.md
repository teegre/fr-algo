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

Attention si l'on affecte une chaîne de longueur différente,
la valeur est soit tronquée, soit des espaces sont ajoutés à
la fin. En d'autres termes, une variable de type Caractère aura
toujours la même longueur, peu importe sa valeur.

Exemple :

```
Variable c en Caractère*5
c <- "ABC"
Longueur(c) = 5
# VRAI
# c → "ABC  "
c <- "ABCDEF"
Longueur(c) = 5
# VRAI
# c → "ABCDE"
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

```
Tableau t1[4] en Entier
Tableaux u[], v[1,1], w[7,7,7] en Entier
# Affectation
t[0] <- 1
t[1] <- 2
t[2] <- 3
t[3] <- 4
# Redimensionnement
Redim u[4]
u <- t
u = t
# VRAI
v[0,0] <- 1
v[0,1] <- 2
...
w[0,0,0] <- 1
...
w[7,7,7] <- 512
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
```

### Manipulations de chaînes de caractères

```
# Longueur renvoie la longueur d'une chaîne de caractères.
Longueur("ABC")
# 3
#
# Extraire renvoie une sous-chaîne contenue dans une chaîne selon un
# index et une longueur donnés.
Extraire("Carte de crédit", 1, 5)
# Carte
#
# Gauche renvoie la sous-chaîne d'une longueur donnée à partir du
# début d'une chaîne.
Gauche("Carte de crédit", 5)
# Carte
# Droite renvoie la sous-chaîne d'une longueur donnée à partir de
# la fin d'une chaîne.
Droite("Carte de crédit", 6)
# crédit
# Trouve renvoie l'index d'une sous-chaîne dans une chaîne.
Trouve("Carte de crédit", "crédit")
# 10
```

### Lecture / Ecriture de fichiers texte


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
Tableau t[7]
Taille(t)
# 8
```
