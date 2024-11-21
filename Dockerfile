# Set the base image to use to py3.9
FROM python:3.11.7-slim-bullseye

#Disable buffering to stdin/stdout
ENV PYTHONUNBUFFERED=1

# Set the file maintainer
LABEL org.opencontainers.image.authors="mark@markciecior.com"

# Set env variables used in this Dockerfile (add a unique prefix, such as DOCKYARD)
# Directory in container for all project files
ENV DOCKYARD_SRVHOME=/srv

COPY requirements.txt $DOCKYARD_SRVHOME/requirements.txt

RUN apt-get update && \
    apt-get -y install curl \
    cron \
    nginx \
    nano \
    bash \
    dos2unix \
    procps

RUN buildDeps='gcc g++ libc6-dev make' && \
    apt-get install -y $buildDeps && \
    python3 -m pip install --no-cache-dir -r $DOCKYARD_SRVHOME/requirements.txt && \
    apt-get purge -y --auto-remove $buildDeps && \
    rm -rf /var/lib/apt/lists/*


# Create application subdirectories
RUN mkdir $DOCKYARD_SRVHOME/media
RUN mkdir $DOCKYARD_SRVHOME/static
RUN mkdir $DOCKYARD_SRVHOME/logs

# Set timezone
RUN cp /usr/share/zoneinfo/America/Chicago /etc/localtime

# Port to expose
EXPOSE 80

# Copy entrypoint script into the image
COPY docker-entrypoint.sh /
RUN dos2unix docker-entrypoint.sh
RUN chmod +x docker-entrypoint*.sh
COPY django_nginx.conf /etc/nginx/sites-available/
COPY nginx.conf /etc/nginx/

# Copy application source code to SRCDIR
COPY mysite $DOCKYARD_SRVHOME/mysite
COPY voting4h $DOCKYARD_SRVHOME/voting4h
COPY manage.py $DOCKYARD_SRVHOME/manage.py

# Start container
WORKDIR $DOCKYARD_SRVHOME
RUN mkdir -p /etc/nginx/sites-enabled/
RUN ln -s /etc/nginx/sites-available/django_nginx.conf /etc/nginx/sites-enabled/
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
