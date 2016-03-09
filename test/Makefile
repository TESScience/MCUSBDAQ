.PHONY: all

all: venv

venv: requirements.txt
	[ -d $@ ] || virtualenv -p $(shell which python2.7) $@
	$@/bin/pip install -r $<
	touch $@

clean:
	rm -rf venv
