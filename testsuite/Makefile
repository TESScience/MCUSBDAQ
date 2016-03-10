.PHONY: all install

all: install

.venv-clean: requirements.txt
	[ -d $@ ] || virtualenv -p $(shell which python2.7) $@
	$@/bin/pip install -r $<
	touch $@

venv: .venv-clean
	rm -rf $@
	$</bin/virtualenv-clone $< $@
	(cd .. ; $(CURDIR)/$@/bin/python setup.py install)

install: venv

reinstall:
	rm -rf venv
	make venv

clean:
	rm -rf venv .venv-clean
