# Install Debian package dependencies and create user account.
FROM debian:bookworm AS base
ARG DEBIAN_FRONTEND=noninteractive
RUN groupadd myuser && useradd -m -s /bin/bash -g myuser myuser
RUN apt update && \
    apt upgrade -y && \
    apt install -y ca-certificates curl libpq5 nano python3-pip python3-venv tmux
COPY ./unit.d/nginx-keyring.gpg /usr/share/keyrings/
COPY ./unit.d/unit.list /etc/apt/sources.list.d/
RUN apt update && \
    apt install -y unit unit-python3.11

# Create the Python virtual environment and install the webserver
# there.
FROM base AS builder
USER myuser
WORKDIR /home/myuser/
COPY --chown=myuser:myuser ./webserver ./webserver-tmp
RUN python3 -m venv ./webserver-venv && \
    ./webserver-venv/bin/pip install ./webserver-tmp

# Copy the virtual environment, all the configuration files, and
# launch.
FROM base AS final
USER root
WORKDIR /root/
COPY --from=builder --chown=myuser:myuser /home/myuser/webserver-venv /home/myuser/webserver-venv
COPY --chmod=0600 --chown=myuser:myuser ./unit.d/.pgpass /home/myuser
COPY ./unit.d/unit.json /etc/
COPY --chmod=744 ./unit.d/entrypoint.sh ./unit.d/reload.sh ./
ENTRYPOINT ["./entrypoint.sh"]
