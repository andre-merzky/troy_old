
all: pics
	@cd .. && epydoc -v --config=docs/epydoc.troy.pilot.cfg

pics:
	@fig2dev -Lpdf architecture.fig     architecture.pdf
	@fig2dev -Lpdf architecture_alt.fig architecture_alt.pdf
	@rm -f *.fig.bak

