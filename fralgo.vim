" Vim syntax file
" Language: ALGO
" Maintainer: Stéphane MEYER (Teegre)
" Last change: 2024/04/08

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
syn match BinOp "dp"
