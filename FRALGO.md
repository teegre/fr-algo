# FRALGO

## Types de données

```
Booléen
# VRAI ou FAUX
Entier
# 1, -6, 33
Numérique
# 1.2, -3.4, 5.67
Chaîne
# "Bonjour"
```

## Variables

```
Variable a en Entier
Variables c1, c2, c3 en Chaîne
a <- 12
c1 <- "Chaîne1"
c2 <- "Chaîne2"
c3 <- c1 & " " & c2
```

## Tableaux

```
Tableau t[4] en Entier
Tableaux u[], v[1,1], w[7,7,7] en Entier
# Affectation
t[0] <- 1
t[1] <- 2
t[2] <- 3
t[3] <- 4
# Redimensionnement
Redim u[4]
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
dp
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

### Manipulations de chaînes de caractères

```
# Longueur renvoie la longueur d'une chaîne de caractères.
Longueur("ABC")
# 3
# Extraire renvoie une sous-chaîne contenue dans une chaîne selon un index et une longueur donnés.
Extraire("Carte de crédit", 1, 5)
# Carte
# Gauche renvoie la sous-chaîne d'une longueur donnée à partir du début d'une chaîne.
Gauche("Carte de crédit", 5)
# Carte
# Droite renvoie la sous-chaîne d'une longueur donnée à partir de la fin d'une chaîne.
Droite("Carte de crédit", 6)
# crédit
# Trouve renvoie l'index d'une sous-chaîne dans une chaîne.
Trouve("Carte de crédit", "crédit")
# 10
```

### Conversion de types de données

```
Chaîne(123)
# "123"
Chaîne(1.23)
# "1.23"
Entier("123")
# 123
Numérique("1.23")
# 1.23
```
