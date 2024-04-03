# FRALGO

**FRALGO** (prononcé *F-R-ALGO*) est un interpréteur et REPL pour le pseudo-langage de programmation **Algo**.

## Utilisation

Il existe deux programmes en ligne de commande : **fralgo** et **fralgorepl**.

Le premier permet d'exécuter un programme **Algo** préalablement enregistré dans un fichier.

Le second est un **REPL** (**R**ead-**E**val-**P**rint-**L**oop) , en français : *boucle de lecture, d'évaluation et d'affichage*. C'est un __environnement interactif__ qui permet d'exécuter des expressions écrites en **Algo**.

### fralgo

`fralgo <fichier>`

où `<fichier>` est le chemin vers un fichier contenant un programme écrit en **Algo**.

#### Exemple

```
Début
  Ecrire "Bonjour le monde !"
Fin
```

Pour exécuter le programme ci-dessus enregistré dans le fichier *bonjour.algo*, il suffit d'entrer cette commande dans un terminal :

`$ fralgo bonjour.algo`

Après un appui sur la touche <kbd>Entrée</kbd>, l'on obtient :

```shell
$ fralgo bonjour.algo
Bonjour le monde !
$
```

### fralgorepl

Pour charger **l'environnement interactif**, entrer la commande suivante :

`$ fralgorepl`

```
$ fralgorepl
 _______ ______ _______ _____   _______ _______ 
|    ___|   __ \   _   |     |_|     __|       |
|    ___|      <       |       |    |  |   -   |
|___|   |___|__|___|___|_______|_______|_______|
A L G O R I T H M E S                   0.10.4mg

[ ctrl+d pour quitter ]
En attente de vos instructions.

:::
```

Chaque expression sera evaluée après l'appui sur la touche <kbd>Entrée</kbd>

#### Exemple

```
$ fralgorepl
 _______ ______ _______ _____   _______ _______ 
|    ___|   __ \   _   |     |_|     __|       |
|    ___|      <       |       |    |  |   -   |
|___|   |___|__|___|___|_______|_______|_______|
A L G O R I T H M E S                   0.10.4mg

[ ctrl+d pour quitter ]
En attente de vos instructions.

::: Ecrire "Bonjour le monde !"
Bonjour le monde !
:::
```

## Syntaxe

La syntaxe est globalement similaire à celle du cours à quelques exceptions près qui seront évoquées plus loin dans ce document.

Elle doit être scrupuleusement appliquée sous peine d'avoir des erreurs lors de l'exécution des programmes !

Les <u>mots reservés</u> sont <u>sensibles à la casse</u> et aux <u>accents</u>, par exemple :

`Debut`, `debut`, `Début` seront traîtés différemment par l'interpréteur. En effet, si `Début` est un mot reservé indiquant le commencement d'un programme **Algo**, `Debut` et `debut` sont considérés comme des <u>variables</u>.

Il est à noter que **chaque instruction d'un programme Algo**, s'il se trouve dans un fichier, **doit être suivie d'un et un seul retour à la ligne** et les éventuels sauts de ligne après le mot réservé `Fin` provoquent une erreur de syntaxe.

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

Les commentaires en fin de ligne ne sont pas acceptés.

## Types de données

**Algo** comprend en tout 4 **types de données** :

`Entier` : un nombre entier `0`, `72`, `-5`, `33`.

`Numérique` : un nombre à virgule flottante `0.1`, `-32.45`, `9.99`

`Chaîne` : une chaîne de caractères `"Marchandise"`, `"Spectacle"`

`Caractère` : un caractère `"A"`, `"z"`  
Il est également possible d'en spécifier la longueur (voir plus bas).

`Booléen`: `VRAI` ou `FAUX`.

## Variables

### Déclaration

Toute variable doit être préalablement déclarée avant de pouvoir être utilisée. Il existe deux manières de déclarer des variables :

`Variable a en Entier` : déclare une variable `a` de type `Entier`.

`Variables c1, c2, c3 en Chaîne` : déclare 3 variables `c1`, `c2` et `c3` de type `Chaîne`.

### Déclaration d'une variable de type Caractère

Comme indiqué plus haut, les variables de type `Caractère` peuvent être dimensionnées. Par défaut, ce type de variable ne peut contenir qu'un unique caractère :

`Variable car en Caractère`

Pour déclarer une variable d'une longueur prédéfinie, la syntaxe est la suivante :

`Variable car*12 en Caractère`

**Avertissement** : une variable de type `Caractère` aura toujours la même longueur. Par exemple, si l'on affecte `"Bonjour"` à la variable `car`, son contenu sera égal à `"Bonjour     "`. De même que si on lui affecte `"BonjourBonjour"`, soit <u>15 caractères</u>, son contenu sera **tronqué** en `"BonjourBonjo"`, soit <u>exactement 12 caractères</u>.

### Affecter une valeur à une variable

Pour affecter une valeur à une variable, on utilise l'opérateur `←` ou `<-` indifféremment. Par exemple :

`a <- 12`

`c1 <- "Algo"`

Il est bien évidemment possible d'affecter le résultat d'une expression à une variable :

`a ← b + 10`

## Tableaux (variables indexées)



## Lecture / Ecriture

### Ecrire

Pour afficher à l'écran des expressions, le contenu de variables ou simplement du texte, on utilise l'instruction `Ecrire`.

Exemple :

```
Ecrire "Bonjour le monde !"
```

Pour afficher plusieurs éléments à la fois, on les sépare par des virgules :

```
Variables nom, prenom en Chaîne
Début
  nom <- "Croisille"
  prenom <- "Nicole"
  Ecrire "Bonjour,", prenom, nom, "!"
Fin
```

Un espace est automatiquement ajouté entre les éléments affichés.

De plus l'instruction `Ecrire` ajoute un saut de ligne à la fin de la chaîne affichée.

```
Bonjour, Nicole Croisille
_
```

Dans certaines situations il sera nécessaire de ne pas afficher ce saut de ligne.

Pour ce faire, il suffira d'ajouter le caractère `\` à la fin de l'instruction `Ecrire` :

```
Ecrire "Bonjour,", prenom, nom, ", " \
Ecrire "ravi de vous rencontrer."
```

Ce qui aura pour résultat :

```
Bonjour, Nicole Croisille, ravi de vous rencontrer.
_
```

### Lire

L'instruction `Lire` permet d'affecter à une variable des données saisies par un utilisateur.

```
Lire n
```

Les données saisies étant systématiquement de type `Chaîne`, **Fralgo** essaiera automatiquement de convertir ce qui a été saisi dans le type attendu par la variable.

```
Variable n en Entier
...
Lire n
```
