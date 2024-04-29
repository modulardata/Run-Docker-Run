# Write the codes below!
FROM python:3.11-slim

# Expose port 8000
EXPOSE 8000

# Set the working directory to /home/app
WORKDIR /home/app

# Add the content of the hyper-app directory to the working directory
ADD hyper-app /home/app

# Install dependencies
RUN pip install -r requirements.txt

# Set the entrypoint to run the main.py file
ENTRYPOINT ["python3", "main.py"]
