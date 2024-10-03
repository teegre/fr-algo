" Vim syntax file
" Language: ALGO
" Maintainer: Stéphane MEYER (Teegre)
" Last change: 2024/05/28

if exists("b:current_syntax")
  finish
endif

syn case match

" ========================================================================================


syn match BinOp "\-"
syn match BinOp "+"
syn match BinOp "\*"
syn match BinOp "\/"
syn match BinOp "%"
syn match BinOp "\<DP\>"
syn match BinOp "\^"
syn match BinOp "<"
syn match BinOp "<="
syn match BinOp ">"
syn match BinOp ">="
syn match BinOp "<>"
syn match BinOp "&"
syn match BinOp "\<ET\>"
syn match BinOp "\<OU\>"
syn match BinOp "\<OUX\>"

syn match Assignment "←\|<-"

syn keyword Import Importer Alias
syn keyword VarDeclaration Variable Variables Tableau Tableaux
syn keyword Structure Structure FinStructure Table FinTable
syn keyword VarType Booléen Caractère Chaîne Entier Numérique
syn keyword Program Début Fin
syn keyword Library Librairie Initialise
syn keyword File Ajout Ecriture Lecture
syn keyword Func Fonction Retourne FinFonction
syn keyword Proc Procédure FinProcédure
syn keyword StockFunc Aléa Car Clefs CodeCar Dormir Droite Ecrire EcrireErr EcrireFichier Existe
syn keyword StockFunc Extraire FDF Fermer Gauche Lire LireFichier Longueur NON Ouvrir Redim Taille
syn keyword StockFunc Valeurs TempsUnix Trouve Type
syn keyword Loop TantQue FinTantQue Pour Suivant
syn keyword Condition Si Alors SinonSi Sinon FinSi
syn keyword Bool VRAI FAUX
syn keyword Conjonction à en sur
syn keyword Arguments _ARGS Clef Valeur
syn region AlgoString start='"' skip=/\v\\./ end='"'
syn region AlgoString start="'" skip=/\v\\./ end="'"

syn keyword AlgoTodo TODO FIXME NOTE NOTES contained
syn match AlgoComment "#.*" contains=Todo

syn match ID "\v[a-zA-Zàéè_(][a-zA-Z0-9-_:)]*" display contained

syn match AlgoNumber "\<\d\+"
syn match AlgoNumber "[-]\d\+"
syn match AlgoNumber "\<\d\+\.\d*"
syn match AlgoNumber "[-]\d\+\.\d*"

syn sync lines=100

let b:current_syntax = "algo"

hi def link Program Constant
hi def link Library Constant
hi def link Assignment Constant
hi def link Arguments Constant
hi def link StockFunc Keyword
hi def link Func PreProc
hi def link Proc PreProc
hi def link BinOp Operator
hi def link Condition Conditional
hi def link VarType Type
hi def link Bool Boolean
hi def link AlgoString String
hi def link AlgoNumber Number
hi def link File PreProc
hi def link ID Identifier
hi def link Import Include
hi def link VarDeclaration Statement
hi def link Structure Structure
hi def link AlgoComment Comment
hi def link AlgoTodo Todo
hi def link Loop Repeat
hi def link Conjonction Constant
