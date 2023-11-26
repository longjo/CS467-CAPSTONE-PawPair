#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Kill any running instances of the app (replace 'app.py' with the name of your app file)
pkill -f app.py

# Set Flask environment variables
export FLASK_APP=app.py
export FLASK_ENV=development

# Start Flask app
flask run
