FROM python:3.11-slim

# Install dependencies for building uwsgi
RUN apt update
RUN apt install -y build-essential python3.11-dev libpcre3 libpcre3-dev

# Copy application code and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Setup user
ARG user=flaskapp
ARG group=flaskapp
ARG uid=1000
ARG gid=1000
RUN groupadd -g ${gid} ${group}
RUN useradd -u ${uid} -g ${gid} -s /bin/sh -d /app ${user}

# Switch to flask app user
USER ${user}
WORKDIR /app
COPY --chown=${user}:${group} DataMaintenance DataMaintenance
COPY --chown=${user}:${group} *.py ./
COPY --chown=${user}:${group} *.ini ./
COPY --chown=${user}:${group} start_service.sh ./
COPY --chown=${user}:${group} crontab_sync_nhi ./

# Port 6400 is the flask service port
EXPOSE 6400

# Start sync script
RUN chmod +x ./start_service.sh

# Start app
ENTRYPOINT ["./start_service.sh"]