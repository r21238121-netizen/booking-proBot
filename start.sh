#!/bin/bash

# Production startup script for TonLucky bot

set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting TonLucky production deployment..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    exit 1
fi

# Load environment variables
export $(grep -v '^#' .env | xargs)

# Check if required environment variables are set
if [ -z "$BOT_TOKEN" ]; then
    echo "Error: BOT_TOKEN is not set in .env file!"
    exit 1
fi

if [ -z "$DATABASE_URL" ]; then
    echo "Error: DATABASE_URL is not set in .env file!"
    exit 1
fi

# Install dependencies if not already installed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

source venv/bin/activate

# Upgrade pip and install requirements
pip install --upgrade pip
pip install -r requirements.txt

echo "Starting bot with production settings..."

# Start the bot
python -m bot.main