#!/bin/bash
# -----------------------------------------------------------------
# Script Name: upload_to_pypi.sh
# Description: This script automates the process of packaging and 
#              uploading a Python project to PyPI (Python Package Index).
# Usage: ./upload_to_pypi.sh
# Dependencies: Ensure Python and twine are installed and configured properly.
# -----------------------------------------------------------------

# Step 1: Create distribution packages for the project.
# The 'sdist' command creates a source distribution, and 'bdist_wheel'
# creates a built distribution. The built distribution is platform-specific.
echo "Creating distribution files..."
python setup.py sdist bdist_wheel

# Check if the previous step succeeded before proceeding.
if [ $? -ne 0 ]; then
    echo "Failed to create distribution files. Exiting."
    exit 1
fi

# Step 2: Upload the created distribution files to PyPI using twine.
# 'dist/*' specifies that all files in the 'dist' directory should be uploaded.
echo "Uploading distribution files to PyPI..."
twine upload dist/*

# Check if the upload was successful.
if [ $? -ne 0 ]; then
    echo "Failed to upload files to PyPI. Check the error messages above."
    exit 1
else
    echo "Files successfully uploaded to PyPI."
fi