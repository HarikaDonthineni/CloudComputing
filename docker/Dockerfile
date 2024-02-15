# Dockerfile
FROM python:3.9-slim

# Create the directory structure
RUN mkdir -p /home/data /home/output

# Copy files into the container image
COPY /IF.txt /home/data/IF.txt
COPY /Limerick-1.txt /home/data/Limerick-1.txt
# Copy the Python script into the container
COPY script.py /home/script.py

# Set the working directory
WORKDIR /home

# Command to run the Python script
CMD ["python", "/home/script.py"]