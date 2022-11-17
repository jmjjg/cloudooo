FROM ubuntu:20.04

SHELL ["/bin/bash", "-eou", "pipefail", "-c"]

RUN apt-get update \
    && apt-get install --assume-yes \
        software-properties-common=0.99.9.8 \
    && add-apt-repository ppa:libreoffice/libreoffice-7-0 --yes \
    && echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | debconf-set-selections \
    && apt-get install --assume-yes \
        libcairo2=1.16.0-4ubuntu1 \
        libcups2=2.3.1-9ubuntu1.2 \
        libgl1-mesa-dev=21.2.6-0ubuntu0.1~20.04.2 \
        libpython2.7=2.7.18-1~20.04.3 \
        libreoffice-calc=1:7.0.6-0ubuntu0.20.04.1~lo1 \
        libreoffice-draw=1:7.0.6-0ubuntu0.20.04.1~lo1 \
        libreoffice-impress=1:7.0.6-0ubuntu0.20.04.1~lo1 \
        libreoffice-writer=1:7.0.6-0ubuntu0.20.04.1~lo1 \
        libsm6=2:1.2.3-1 \
        libxinerama1=2:1.1.4-2 \
        libxml2-dev=2.9.10+dfsg-5ubuntu0.20.04.4 \
        libxslt1-dev=1.1.34-4ubuntu0.20.04.1 \
        python-libxml2=2.9.10+dfsg-5ubuntu0.20.04.4 \
        python-lxml=4.5.0-1ubuntu0.5 \
        python-psutil=5.5.1-1ubuntu4 \
        python-setuptools=44.0.0-2 \
        python-zope.interface=4.7.1-1 \
        python2.7=2.7.18-1~20.04.3 \
        python2.7-dev=2.7.18-1~20.04.3 \
        ttf-mscorefonts-installer=3.7ubuntu6 \
        wget=1.20.3-1ubuntu2 \
    && rm --recursive /var/lib/apt/lists/* \
    && ln --symbolic /usr/bin/python3 /usr/lib/libreoffice/program/python

COPY . /opt/cloudooo
COPY ./docker/etc/cloudooo.conf /etc/cloudooo.conf

WORKDIR /opt/cloudooo/

#RUN python2 setup.py install
RUN wget https://bootstrap.pypa.io/pip/2.7/get-pip.py --output-document /tmp/get-pip.py --quiet \
    && python2 /tmp/get-pip.py \
    && rm /tmp/get-pip.py \
    && pip install --no-cache-dir --requirement requirements.txt

EXPOSE 8011

CMD ["/bin/bash", "-eou", "pipefail", "-c", "/usr/local/bin/paster serve /etc/cloudooo.conf --daemon --pid-file /var/run/cloudooo.pid --log-file=/var/log/cloudooo.log && tail -f /var/log/cloudooo.log"]
