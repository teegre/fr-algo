" Vim syntax file
" Language: ALGO
" Maintainer: Stéphane MEYER (Teegre)
" Last change: 2024/04/09

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
syn match BinOp "DP"
syn match BinOp "\^"
syn match BinOp "<"
syn match BinOp "<="
syn match BinOp ">"
syn match BinOp ">="
syn match BinOp "<>"
syn match BinOp "&"
syn match BinOp "ET"
syn match BinOp "OU"
syn match BinOp "OUX"

syn match Assignment "←\|<-"

syn keyword VarDeclaration Variable Variables Tableau Tableaux Structure FinStructure
syn keyword VarType Booléen Caractère Chaîne Entier Numérique
syn keyword Program Début Fin
syn keyword File Ajout Ecriture Lecture
syn keyword Func Fonction Retourne FinFonction
syn keyword StockFunc Aléa Droite Ecrire EcrireFichier Extraire FDF Fermer
syn keyword StockFunc Gauche Lire LireFichier Longueur NON Ouvrir Redim Trouve
syn keyword Loop TantQue FinTantQue Pour Suivant
syn keyword Condition Si Alors SinonSi Sinon FinSi
syn keyword Bool VRAI FAUX
syn keyword Conjonction à en sur
syn region AlgoString start='"' skip=/\v\\./ end='"'
syn region AlgoString start="'" skip=/\v\\./ end="'"

syn keyword AlgoTodo TODO FIXME NOTE NOTES contained
syn match AlgoComment "#.*" contains=Todo

syn match ID "\v[a-zA-Zàéè_(][a-zA-Z0-9-_:)]*" display contained

" syn keyword powStatement def  nextgroup=powID skipwhite 
" syn keyword powStatement set  nextgroup=powID skipwhite
" syn keyword powStatement setg nextgroup=powID skipwhite

syn match AlgoNumber "\<\d\+"
syn match AlgoNumber "[-]\d\+"
syn match AlgoNumber "\<\d\+\.\d*"
syn match AlgoNumber "[-]\d\+\.\d*"

syn sync lines=100

let b:current_syntax = "algo"

hi def link Program Constant
hi def link Assignment Constant
hi def link StockFunc Keyword
hi def link Func PreProc
hi def link BinOp Operator
hi def link Condition Conditional
hi def link VarType Type
hi def link Bool Boolean
hi def link AlgoString String
hi def link AlgoNumber Number
hi def link File PreProc
hi def link ID Identifier
hi def link VarDeclaration Statement
hi def link AlgoComment Comment
hi def link AlgoTodo Todo
hi def link Loop Statement
hi def link Conjonction Constant
