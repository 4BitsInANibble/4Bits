#!/bin/bash

# Exit on any error
set -e

# Check for Python and pip
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install it before running this script."
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. Please install it before running this script."
    exit 1
fi

# Install Tesseract OCR if not already installed
if ! command -v tesseract &> /dev/null; then
    echo "Tesseract OCR is not installed. Installing..."
    sudo apt-get update
    sudo apt-get install tesseract-ocr -y
fi

# Install required Python packages for both scripts
pip3 install pillow pytesseract openai

# Run the test OCR script, we prioritze tesseract
python3 test_pytesseract.py

# Run the OpenAI GPT-3.5 script
# Make sure to replace YOUR_OPENAI_API_KEY with your actual API key
export OPENAI_API_KEY='YOUR_OPENAI_API_KEY'
python3 ai_recipe_rec.py

