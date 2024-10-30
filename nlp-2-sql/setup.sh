#!/bin/bash

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Install spaCy model
echo "Installing spaCy model..."
python -m spacy download en_core_web_sm

echo "Setup completed!"