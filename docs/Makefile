
all:
	rm -f *.pdf ; 
	for f in *fig; do echo $$f ; fig2dev -Lpdf $$f $$f.pdf ; done; 
	mmv \*.fig.pdf \#1.pdf

clean:
	rm *.bak

