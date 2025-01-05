#!/bin/bash

# Script to set up the environment and schedule main.py with user's cron

echo "Updating package list..."
sudo apt update

echo "Installing Python3 and pip3..."
sudo apt install -y python3 python3-pip

echo "Removing EXTERNALLY-MANAGED restriction..."
sudo rm /usr/lib/python3.11/EXTERNALLY-MANAGED

echo "Installing necessary Python libraries..."
pip3 install bleak paho-mqtt netifaces

# Ensure the main.py file is executable
echo "Making main.py executable..."
chmod +x "$(pwd)/main.py"

# Get the current directory
current_dir=$(pwd)

# Schedule the script with cron for the current user
echo "Adding main.py to user's cron (every 10 minutes)..."
(crontab -l 2>/dev/null; echo "*/10 * * * * python3 $current_dir/main.py") | crontab -

echo "Setup completed successfully! main.py will run every 10 minutes."
