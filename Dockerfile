FROM python:3.10-alpine

# Set working directory
RUN mkdir /app
WORKDIR /app

# Copy application code and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY DataMaintenance DataMaintenance
COPY *.py ./
COPY start_service.sh ./

# Port 6400 is the flask service port
EXPOSE 6400

# Start sync script
RUN chmod +x ./start_service.sh


# Start app
ENTRYPOINT ["./start_service.sh"]