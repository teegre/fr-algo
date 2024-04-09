" Vim syntax file
" Language: ALGO
" Maintainer: Stéphane MEYER (Teegre)
" Last change: 2024/04/09

if exists("b:current_syntax")
  finish
endif

syn case match

" ========================================================================================

syn match BinOp "\v-\s"
syn match BinOp "\v\+\s"
syn match BinOp "\v*\s"
syn match BinOp "\v/"
syn match BinOp "%"
syn match BinOp "Dp"
syn match BinOp "\^"
syn match BinOp "<"
syn match BinOp "<="
syn match BinOp ">"
syn match BinOp ">="
syn match BinOp "<>"
syn match BinOp "\vET\s"
syn match BinOp "\vOU\s"
syn match BinOp "\vOUX\s"

syn match Assignment "←|<-"

syn keyword VarDeclaration Variable Variables Tableau Tableaux
syn keyword VarType Booléen Caractère Chaîne Entier Numérique
syn keyword Program Début Fin
syn keyword StockFunc Aléa Droite Ecrire EcrireFichier Extraire FDF Fermer
syn keyword StockFunc Gauche Lire LireFichier Longueur Ouvrir Redim Trouve
syn keyword Loop TantQue FinTanque Pour Suivant
syn keyword Conditional Si Alors SinonSi Sinon FinSi
syn keyword Boolean VRAI FAUX

syn region String start='"' skip=/\v\\./ end='"'
syn region String start="'" skip=/\v\\./ end="'"

syn keyword Todo TODO FIXME NOTE NOTES contained
syn match Comment "#.*" contains=Todo

syn match ID "\v[a-zA-Zàéè_(][a-zA-Z0-9-_:)]*" display contained

" syn keyword powStatement def  nextgroup=powID skipwhite 
" syn keyword powStatement set  nextgroup=powID skipwhite
" syn keyword powStatement setg nextgroup=powID skipwhite

" syn match   powLambda "\v\@[a-zA-Z_][a-zA-Z0-9-_]*" display contained

" syn keyword powLambdaCall @ nextgroup=powLambda skipwhite

" syn match powNumber "\<\d\+"
" syn match powNumber "[-]\d\+"
" syn match powNumber "\<\d\+\.\d*"
" syn match powNumber "[-]\d\+\.\d*"

" syn match powOp   "\v1\v\+"
" syn match powOp   "\v1\v-"

" syn sync lines=100

" hi def link powFunc       Keyword
" hi def link powOp         Operator
" hi def link powCond       Conditional
" hi def link powType       Type
" hi def link powBool       Boolean
" hi def link powString     String
" hi def link powNumber     Number
" hi def link powID         Identifier
" hi def link powLambda     Identifier
" hi def link powLambdaCall Identifier
" hi def link powStatement  Statement
" hi def link powComment    Comment
" hi def link powTodo       Todo

" let b:current_syntax = "pow"
