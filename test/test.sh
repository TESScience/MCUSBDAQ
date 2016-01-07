#!/bin/bash -x
set -euo pipefail

rm -rf venv
if [ ! -d venv-back ] ; then
	virtualenv venv
	mv venv venv-back
fi
cp -a venv-back venv
(cd ..; ./test/venv/bin/python setup.py install)
./venv/bin/python test.py
