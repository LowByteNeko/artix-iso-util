#!/bin/sh

python -m build
cd dist || exit
pip install --force-reinstall ./artix_iso_util-*-py3-none-any.whl
cd ..
rm -r dist
