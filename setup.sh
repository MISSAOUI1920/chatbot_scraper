#!/bin/bash

# Install system dependencie
apt-get update
apt-get install -y build-essential  # Ensure build tools are available

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt  # Ensure all Python packages are installed

# Additional setup commands as needed
python -m nltk.downloader punkt  # Download NLTK resources
python -m spacy download en_core_web_sm  # Download spaCy model
