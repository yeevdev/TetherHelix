#!/bin/bash

rm -rf tetherhelix_pyenv
python3 -m venv tetherhelix_pyenv && source tetherhelix_pyenv/bin/activate && pip install -r requirements.txt
