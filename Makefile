
all: doc

doc:
	@make -C docs html

clean:
	@find . -name \*.pyc      -exec rm {} \;
	@find . -name \*.bak      -exec rm {} \;
	@find . -name .\*.sw[o-z] -exec rm {} \;
	@rm -rf docs/_build/*
	@rm -rf /tmp/peejay/*
	@rm -rf $(HOME)/.bigjob/
	@ps -ef | grep basic_peejay.py | grep -v grep | cut -c 10-15 | xargs -r -t kill


sync:
	-@git co devel
	-@git branch -D gh-pages
	-@git branch gh-pages
	-@git push


