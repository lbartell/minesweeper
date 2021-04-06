#!/bin/bash

# Create virtual environment
python -m venv .venv

# Upgrade pip and install depenencies in environment
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt