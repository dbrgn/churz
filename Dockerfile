FROM python:3.10-slim-bullseye

# Add code
ADD . /app/
WORKDIR /app/

# Install init process and other dependencies
RUN apt-get update -q \
 && apt-get -y -q install --no-install-recommends dumb-init \
 && rm -rf /var/lib/apt/lists/*

# Add non-root user
RUN addgroup --gid 14327 churz \
 && adduser --disabled-password --gecos "" --uid 14327 --gid 14327 churz

# Set up directories
RUN chown -R churz:churz /app/ \
 && chmod 0700 /app/
RUN mkdir /var/venv \
 && chown churz:churz /var/venv
VOLUME /var/data

# Drop root permissions
USER churz

# Install dependencies
RUN python3 -m venv /var/venv \
 && /var/venv/bin/pip install -U pip
RUN /var/venv/bin/pip install -r requirements.txt

# Expose port
EXPOSE 9393

# Note: Use dumb-init in order to fulfil our PID 1 responsibilities,
# see https://github.com/Yelp/dumb-init
ENTRYPOINT [ "/usr/bin/dumb-init", "--" ]
CMD [ "/var/venv/bin/python", "churz.py", "-l", "0.0.0.0", "-d", "/var/data/churz.json" ]
