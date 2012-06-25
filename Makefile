
all:
	@make -C docs

clean:
	@find . -name \*.pyc      -exec rm {} \;
	@find . -name .\*.sw[o-z] -exec rm {} \;
	@rm -rf docs/troy.pilot/
	@rm -rf /tmp/peejay/*
	@rm -rf $(HOME)/.bigjob/

