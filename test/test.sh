#!/bin/bash +x
set -euo pipefail

rm -rf venv
virtualenv venv
(cd ..; ./test/venv/bin/python setup.py install)
./venv/bin/python test.py
