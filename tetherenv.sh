#!/bin/bash

if { [ "#$" == 0 ]; }; then
    echo "Usage : ./tetherenv.sh [option]"
    exit
fi

if { [ "$1" = "-h" ] || [ "$1" = "--help" ]; }; then
    echo "Tetherhelix Environment Manager v.1.2.1(by ReenAG)"
    echo "Options :"
    echo "-p, --preserve : renew requirement.txt from current environment"
    echo "-h, --help : print this help"
    echo "-e, --enable [option] : enable python environment."
    echo "  [option] : clear : remove this environment compleletely and setup new one. (clear cache)"
    echo ""
    echo "run : enable python environment and run"
    echo "Usage : ./tetherenv.sh [option]"
elif { [ "$1" = "-p" ] || [ "$1" = "--preserve" ]; }; then
    echo "Preserving current libraray settings to requirement.txt. Don't forget to commit!"
    pip list --format=freeze > requirements.txt
elif { [ "$1" == "-e" ] || [ "$1" == "--enable" ]; }; then
    if { [ "$2" == "clear" ]; }; then
        echo "Clearing Currnet Environment..."
        rm -rf .venv
    fi
    echo "Enableing python virtual environment..."
    python3 -m venv .venv && source .venv/bin/activate 
    echo "Installing requrements.txt"
    pip install -r requirements.txt
    echo "Setting is done! Type this command to start."
    echo ""
    echo "source .venv/bin/activate"
    echo ""
elif { [ "$1" == "run" ]; }; then
    python3 -m venv .venv && source .venv/bin/activate
    echo "Starting src/main.py...(venv)"
    python src/main.py
fi
