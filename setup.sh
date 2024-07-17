#!/bin/bash

# Install Python dependencies
pip install --upgrade pip

# Additional setup commands as needed
python -m nltk.downloader punkt  # Download NLTK resources
python -m spacy download en_core_web_sm  # Download spaCy model
