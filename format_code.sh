#!/bin/bash

if ! which yapf &>/dev/null; then
    echo "Install yapf..."
    pip install yapf
fi

yapf -i --style pep8 --recursive .
