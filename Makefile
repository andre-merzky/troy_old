# Makefile for Sphinx documentation
#

all: docs

# You can set these variables from the command line.
SPHINXBUILD   = sphinx-build -a -E -n -c docs/
BUILDDIR      = docs/

.PHONY: docs

docs:
	$(SPHINXBUILD) -b html . $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

clean:
	@rm -rf $(BUILDDIR)/html
	@find . -name \*.pyc -exec rm {} \;

