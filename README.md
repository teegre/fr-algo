# FRALGO

**FRALGO** (prononcé *efferalgo*) est un interpréteur et REPL pour le pseudo-langage de programmation **Algo**.

## Utilisation

Il existe deux programmes en ligne de commande : **fralgo** et **fralgorepl**.

Le premier permet d'exécuter un programme **Algo** préalablement enregistré dans un fichier.

Le second est un **REPL** (**R**ead-**E**val-**P**rint-**L**oop) , en français *boucle de lecture, d'évaluation et d'affichage*. C'est un __environnement interactif__ qui permet d'exécuter des expressions écrites en **Algo**.

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
A L G O R I T H M E S                    0.1.0mg

[ ctrl+d pour quitter ]
En attente de vos instructions.

::>
```

Chaque expression sera evaluée après l'appui sur la touche <kbd>Entrée</kbd>

#### Exemple

```
$ fralgorepl
 _______ ______ _______ _____   _______ _______ 
|    ___|   __ \   _   |     |_|     __|       |
|    ___|      <       |       |    |  |   -   |
|___|   |___|__|___|___|_______|_______|_______|
A L G O R I T H M E S                    0.1.0mg

[ ctrl+d pour quitter ]
En attente de vos instructions.

::> Ecrire "Bonjour le monde !"
Bonjour le monde !
::>
```

## Syntaxe

La syntaxe est globalement similaire à celle du cours à quelques exceptions près qui seront évoquées plus loin dans ce document.

Elle doit être scrupuleusement appliquée sous peine d'avoir des erreurs lors de l'exécution des programmes !

Les <u>mots-clefs</u> sont <u>sensibles à la casse</u> et aux <u>accents</u>, par exemple :

`Debut`, `debut`, `Début` seront traîtés différemment par l'interpréteur. En effet, si `Début` est un mot-clef indiquant le commencement d'un programme **Algo**, `Debut` et `debut` sont considérés comme des <u>variables</u>.

Il est à noter que **chaque instruction d'un programme Algo**, s'il se trouve dans un fichier, **doit être suivie d'un et un seul retour à la ligne** et les éventuels sauts de ligne après le mot-clef `Fin` provoquent une erreur de syntaxe.

## Types de données

**Algo** comprend en tout 4 **types de données** :

`Entier` : un nombre entier `0`, `72`, `-29`, `133`.

`Numérique` : un nombre à virgule flottante `0.1`, `-32.45`, `9.99`

`Chaîne` : une chaîne de caractères `"Chaîne de vélo"`, `"Chaîne hi-fi"`

`Booléen`: `VRAI` ou `FAUX`.

## Variables

### Déclaration

Toute variable doit être au préalable déclarée avant de pouvoir être utilisée. Il existe deux manières de déclarer des variables :

`Variable a en Entier` : déclare une variable `a` de type `Entier`.

`Variables c1, c2, c3 en Chaîne` : déclare 3 variables `c1`, `c2` et `c3` de type `Chaîne`.

### Assigner une valeur à une variable

Pour assigner une valeur à une variable, on utilise l'opérateur `←` ou `<-`, par exemple :

`a <- 12`

`c1 <- "Algo"`

Il est bien évidemment possible d'assigner le résultat d'une expression à une variable :

`a ← b + 10`
