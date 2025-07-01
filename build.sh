#!/usr/bin/env bash

# Update system packages and install ffmpeg
apt-get update && apt-get install -y ffmpeg

# Optional: Make sure pip is up to date
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt
