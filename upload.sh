#!/bin/bash

# Run the setup.py to create distribution files
python setup.py sdist bdist_wheel

# Upload the distribution files to PyPI using twine
twine upload dist/*
