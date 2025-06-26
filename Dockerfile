
#clean environment for docker to run
FROM python:3.11-slim-bookworm

#Update the OS and install security patches
RUN apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

#Create the root directory similar to how app is already structured
WORKDIR /app

#create and enter the backend directory like the app is structured
WORKDIR /app/backend

#copy the backend folder into curr directory
COPY backend/ ./

#install requirements
RUN pip install --no-cache-dir -r requirements.txt

#Expose port 8000 to run the backend server
EXPOSE 8000

#run the backend 
CMD ["python", "app.py"]