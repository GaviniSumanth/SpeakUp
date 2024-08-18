#!/bin/bash

virtualenv .venv
source .venv/bin/activate
pip install tox pre-commit
export PATH=$PATH:$(pwd)/.venv/bin

pre-commit install

pip install -e .
