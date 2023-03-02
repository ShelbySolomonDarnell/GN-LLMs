#! /bin/sh

./scripts/clean.sh
pdflatex -output-format=dvi darnell_shelbysolomon
bibtex darnell_shelbysolomon
pdflatex darnell_shelbysolomon
pdflatex darnell_shelbysolomon
mv darnell_shelbysolomon.pdf out/GeneNetworkOrg-LLM.pdf
./scripts/clean.sh
