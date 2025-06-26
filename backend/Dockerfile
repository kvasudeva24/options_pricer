
#clean environment for docker to run
FROM python:3.11-slim-bookworm

#Update the OS and install security patches
RUN apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

#Create the root directory similar to how app is already structured
WORKDIR /app

#copy the current folder (backend) into curr directory
COPY . .

#install requirements
RUN pip install --no-cache-dir -r requirements.txt

#Expose port 8000 to run the backend server
EXPOSE 8000

#run the backend 
CMD ["python", "app.py"]