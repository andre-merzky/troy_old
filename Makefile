
all:
	@make -C docs

clean:
	@find . -name \*.pyc      -exec rm {} \;
	@find . -name .\*.sw[o-z] -exec rm {} \;
	@rm -rf docs/troy.pilot/
	@rm -rf /tmp/peejay/*
	@rm -rf $(HOME)/.bigjob/

sync:
	@git co devel
	@git ci -am 'sync with gh-pages'
	@git pull
	@git push
	@git co gh-pages
	@git merge devel
	@git push origin gh-pages
	@git co devel


