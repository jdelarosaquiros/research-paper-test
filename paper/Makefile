MAIN = main
TEXFILES = $(wildcard *.tex) $(wildcard sections/*.tex) $(wildcard figs/*.tex)
BIBFILES = $(wildcard *.bib)

.PHONY: build clean watch

build: $(MAIN).pdf

$(MAIN).pdf: $(TEXFILES) $(BIBFILES) neurips_2025.sty
	latexmk -pdf -interaction=nonstopmode -halt-on-error $(MAIN).tex

watch:
	latexmk -pdf -pvc -interaction=nonstopmode $(MAIN).tex

clean:
	latexmk -c
	rm -f *.bbl *.run.xml *.synctex.gz
