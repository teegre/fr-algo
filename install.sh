#! /usr/bin/env bash

version="$(python -c 'from fralgo import __version__; print(__version__.replace(".beta.", "b"))')"
[[ -z $version ]] && {
  echo "Impossible de déterminer la version de FR-ALGO..."
  exit 1
}

echo "o FR-ALGO version ${version}"
echo "* Construction..."
if python -m build &> /dev/null; then
  command -v fralgo &> /dev/null && {
    echo "* Désinstallation de la version précédente..."
    pipx uninstall fralgo &> /dev/null
  }
  echo "* Installation de FR-ALGO..."
  if pipx install "dist/fralgo-${version}.tar.gz" &> /dev/null; then
    echo "* Installation de la librairie standard"
    mkdir -p ~/.local/lib/fralgo 
    git submodule init &> /dev/null
    git submodule update &> /dev/null && \
      cp ./fralgo-std/src/*.algo ~/.local/lib/fralgo/ || stdlib=1
    [[ $stdlib ]] && echo "x L'installation de la librairie standard a échoué."
    echo "o FR-ALGO installé avec succès."
  else
    echo "x L'installation a échoué."
    exit 1
  fi
else
  echo "x La construction a échoué."
  exit 1
fi
