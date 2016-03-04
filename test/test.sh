#!/bin/bash -x
set -euo pipefail
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

rm -rf ${DIR}/venv
if [ ! -d ${DIR}/venv-back ]  ; then
   virtualenv ${DIR}/venv
   mv ${DIR}/venv ${DIR}/venv-back
fi
cp -a ${DIR}/venv-back ${DIR}/venv
(cd ${DIR}/..; rm -rf build ; ${DIR}/venv/bin/python setup.py install)
${DIR}/venv/bin/python ${DIR}/test.py
