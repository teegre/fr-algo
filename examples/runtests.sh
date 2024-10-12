#!/usr/bin/env bash

((counter=1))
((errors=0))

for f in *.algo
do
  echo "${counter}. ${f}"
  python ../fralgo/fralgocli.py  "$f" || ((errors++))
  ((counter++))
done

echo "${counter} tests effectués."
((errors)) || echo "OK"
((errors)) && echo "${errors} erreur(s) rencontrée(s)."
