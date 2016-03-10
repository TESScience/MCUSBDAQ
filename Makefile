.PHONY: all clean testsuite_install testsuite_reinstall install_testsuite reinstall_testsuite

all:

install_testsuite: testsuite_install
testsuite_install: testsuite/venv
testsuite/venv:
	make -C $(dir $@) $(notdir $@)

reinstall_testsuite: testsuite_reinstall
testsuite_reinstall:
	make -C testsuite reinstall

clean:
	make -C testsuite clean
	rm -rf *.pyc $(shell find mcc/ -name "*.pyc") mcc.egg-info/ dist/ build/
