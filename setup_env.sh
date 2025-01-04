#!/bin/bash

# Script to set up the environment and schedule main.py with user's cron

echo "Updating package list..."
sudo apt update

echo "Installing Python3 and pip3..."
sudo apt install -y python3 python3-pip

echo "Installing necessary Python libraries..."
pip3 install bleak paho-mqtt netifaces

# Ensure the main.py file is executable
echo "Making main.py executable..."
chmod +x /home/mfsquare_temp_winti/temp_Sesor/main.py

# Schedule the script with cron for the current user
echo "Adding main.py to user's cron (every 10 minutes)..."
(crontab -l 2>/dev/null; echo '*/10 * * * * python3 /home/mfsquare_temp_winti/temp_Sesor/main.py') | crontab -

echo "Setup completed successfully! main.py will run every 10 minutes."
