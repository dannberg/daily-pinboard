#!/usr/bin/env bash

# Change to the directory where the script is located
cd "$(dirname "$0")"

# Wait for network availability before running the script
MAX_RETRIES=10
RETRY_INTERVAL=10
TRIES=0

echo "[$(date)] Checking network connectivity..." >> /home/dannberg/daily-pinboard/logs.txt

until ping -c1 google.com >/dev/null 2>&1; do
    echo "[$(date)] Network is unavailable. Retrying in $RETRY_INTERVAL seconds..." >> /home/dannberg/daily-pinboard/logs.txt
    TRIES=$((TRIES+1))
    if [ "$TRIES" -ge "$MAX_RETRIES" ]; then
        echo "[$(date)] Network still unavailable after $MAX_RETRIES attempts. Exiting." >> /home/dannberg/daily-pinboard/logs.txt
        exit 1
    fi
    sleep "$RETRY_INTERVAL"
done

echo "[$(date)] Network is available. Running script..." >> /home/dannberg/daily-pinboard/logs.txt

# Activate virtual environment (adjust the path to your virtual environment)
source ${PATH_TO_BASH_SCRIPT}/venv/bin/activate

# Run the Python script
python3 ${PATH_TO_BASH_SCRIPT}/daily-pinboard.py >> ${PATH_TO_BASH_SCRIPT}/logs.txt 2>&1

# Deactivate virtual environment
deactivate
