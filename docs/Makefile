# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXPROJ    = knowlattes
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = build
APIDOC        = sphinx-apidoc
APIDOCDIR     = ./source/api
PROJECTDIR    = ../src/knowlattes

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(O)

.PHONY: help Makefile

apidoc:
	$(APIDOC) -o "$(APIDOCDIR)" "$(PROJECTDIR)"

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile apidoc
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(O)
