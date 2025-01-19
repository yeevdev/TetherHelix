#!/bin/bash

rm -rf tetherhelix_pyenv
python3 -m venv tetherhelix_pyenv && source tetherhelix_pyenv/bin/activate && pip install pyupbit pandas numpy ta requests python-dotenv
