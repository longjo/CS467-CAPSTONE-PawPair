# Set base image (host OS)
FROM python:3.12-alpine

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY app.py .
COPY config.py .

COPY blueprints ./blueprints
COPY static ./static
COPY templates ./templates
COPY utils ./utils

# Specify the command to run on container start
CMD [ "python", "./app.py" ]
# CMD flask run -h 0.0.0.0 -p 5000