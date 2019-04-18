FROM python:3.7.3

ARG BUILD_USER=django
ARG BUILD_USER_GROUP=django
ARG BUILD_USER_PASSWORD=django
ARG BUILD_USER_SHELL=/bin/bash
ARG BUILD_USER_UID=1000
ARG BUILD_USER_GID=1000
ARG BUILD_USER_HOME=/home/django
ARG BUILD_PROJECT_PATH=/opt/django
ARG BUILD_PROJECT_PORT=8000

ENV DJANGO_USER=${BUILD_USER}
ENV DJANGO_USER_GROUP=${BUILD_USER_GROUP}
ENV DJANGO_USER_PASSWORD=${BUILD_USER_PASSWORD}
ENV DJANGO_USER_SHELL=${BUILD_USER_SHELL}
ENV DJANGO_USER_UID=${BUILD_USER_UID}
ENV DJANGO_USER_GID=${BUILD_USER_GID}
ENV DJANGO_USER_HOME=${BUILD_USER_HOME}
ENV PROJECT_PATH=${BUILD_PROJECT_PATH}
ENV PROJECT_PORT=${BUILD_PROJECT_PORT}

# Disable IPv6
RUN echo "Acquire::ForceIPv4 \"true\";" > /etc/apt/apt.conf.d/99force-ipv4

##########################################################################################################
#
#   Creating User Home directory and project folders
#
##########################################################################################################
# Create a dev user to use as the directory owner
RUN set -x \
    && addgroup --gid ${DJANGO_USER_GID} ${DJANGO_USER_GROUP} \
    && adduser --system \
            --uid ${DJANGO_USER_UID} \
            --gid ${DJANGO_USER_GID} \
            --shell ${DJANGO_USER_SHELL} \
            ${DJANGO_USER} \
    && echo "${DJANGO_USER}:${DJANGO_USER_PASSWORD}" | chpasswd

RUN mkdir -p ${PROJECT_PATH}; \
    chown -R "${BUILD_USER}:${BUILD_USER}" ${PROJECT_PATH};

##########################################################################################################
#
#   Installing APP Dependencies
#
##########################################################################################################
RUN apt-get update && apt-get install -y --no-install-recommends -o Acquire::ForceIPv4=true \
        curl \
        git \
        build-essential \
        linux-headers-amd64 \
        postgresql-client \
        postgresql-contrib \
        libpq-dev \
        libpcre3 libpcre3-dev \
        gettext \
        cron \
    ;

RUN pip3 install --upgrade pip

COPY system-requirements.txt /

RUN pip3 install -r /system-requirements.txt

##########################################################################################################
#
#   Installing GOSU
#
##########################################################################################################
ENV GOSU_VERSION 1.10
RUN set -x \
    && apt-get update && apt-get install -y --no-install-recommends ca-certificates wget && rm -rf /var/lib/apt/lists/* \
    && dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')" \
    && wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch" \
    && wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch.asc" \
    && export GNUPGHOME="$(mktemp -d)" \
    && for server in ha.pool.sks-keyservers.net \
              hkp://p80.pool.sks-keyservers.net:80 \
              keyserver.ubuntu.com \
              hkp://keyserver.ubuntu.com:80 \
              pgp.mit.edu; do \
    gpg --keyserver "$server" --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4 && break || echo "Trying new server..."; \
	done \
    && gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu \
    && rm -r "$GNUPGHOME" /usr/local/bin/gosu.asc \
    && chmod +xs /usr/local/bin/gosu \
    && gosu nobody true \
    && apt-get purge -y --auto-remove ca-certificates wget


##########################################################################################################
#
#   Installing SSHD in order to be able debug
#
##########################################################################################################
RUN apt-get update \
    && apt-get install -y openssh-server \
    && mkdir /var/run/sshd \
    && sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd \
    && /usr/bin/ssh-keygen -A


ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

# Cleaning installation files
RUN rm -rf /var/lib/apt/lists/*


##########################################################################################################
#
#   Finishing
#
##########################################################################################################

COPY run.sh /opt/
RUN chown ${BUILD_USER}:${BUILD_USER} /opt/run.sh
RUN chmod +x /opt/run.sh

USER ${BUILD_USER}



##########################################################################################################
#
#   For debug purposes only
#
##########################################################################################################

RUN echo 'db:5432:*:rating:rating' > ~/.pgpass; chmod 600 ~/.pgpass;

WORKDIR ${PROJECT_PATH}

VOLUME ${PROJECT_PATH} /mnt

EXPOSE ${PROJECT_PORT} 22


