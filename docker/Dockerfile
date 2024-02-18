# Dockerfile
FROM python:3.9-slim

# Create the directory structure
RUN mkdir -p /home/data /home/output

# Copy all files in current directory into the container image
COPY . /home/data

# Copy the script into the container
COPY script.py /home/script.py

# Set the working directory
WORKDIR /home

# Command to run the Python script
CMD ["python", "/home/script.py"]