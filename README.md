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
cd fr-algo
```

Enfin, installer **FR-ALGO** à l'aide de la commande suivante :

```
./install.sh
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

`fralgo bonjour.algo`

Après un appui sur la touche <kbd>Entrée</kbd>, nous obtenons :

```
Bonjour le monde !
```

### fralgorepl

Ce programme est un **REPL** (**R**ead-**E**val-**P**rint-**L**oop), en français : **boucle de lecture, d'évaluation et d'affichage**.
C'est un **environnement interactif** qui permet d'exécuter des expressions écrites en **ALGO**.

Pour charger **l'environnement interactif**, entrer la commande suivante :

```
fralgorepl
```

Une invite de commande est alors affichée...

```
 _______ ______        _______ _____   _______ _______
|    ___|   __ \______|   _   |     |_|     __|       |
|    ___|      <______|       |       |    |  |   -   |
|___|   |___|__|      |___|___|_______|_______|_______|
|A|L|G|O|R|I|T|H|M|E|S|        fr-v100 0.12.1.beta.1mg

(c) 2024-2025 Stéphane MEYER (Teegre)

Bonjour, Teegre !
En attente de vos instructions.

:::
```

... Et l'on peut entrer n'importe quelle expression en **ALGO** qui sera exécutée après un appui sur la touche <kbd>Entrée</kbd>

```
 _______ ______        _______ _____   _______ _______
|    ___|   __ \______|   _   |     |_|     __|       |
|    ___|      <______|       |       |    |  |   -   |
|___|   |___|__|      |___|___|_______|_______|_______|
|A|L|G|O|R|I|T|H|M|E|S|        fr-v100 0.12.1.beta.1mg

(c) 2024-2025 Stéphane MEYER (Teegre)

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

## Désinstallation

**Êtes-vous sûr de vouloir désinstaller FR-ALGO ?**

```
pipx uninstall fralgo
rm -rf ~/.local/lib/fralgo
```

## Wiki

Pour plus d'informations, suivez le lien :

[https://github.com/teegre/fr-algo/wiki](https://github.com/teegre/fr-algo/wiki)

