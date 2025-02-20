FROM python:3.11-slim AS base

LABEL run="docker run -tid --rm yankees5963/ha_oilgauge:latest" \
    description="Python Container to send Oil Gauge Stats to MQTT server most often used with HomeAssistant" \
    source="python:3.11-slim" \
    maintainer="holl.william@gmail.com"

ENV LANG C.UTF-8

#Update Image
RUN apt-get -qqy clean; \
    apt-get -qqy update; \
    apt-get -qqy upgrade; \
    apt-get -qqy install gnupg wget curl; \
    rm -rf /tmp/*; \
    rm -rf /root/*;

# Install manually all the missing libraries
RUN apt-get update
RUN apt-get install -y gconf-service libvulkan1 libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils

# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install
RUN rm -rf google-chrome-stable_current_amd64.deb;

#cleanup
RUN apt-get -qqy clean; \
    apt-get -qqy autoremove; \
    rm -rf /tmp/*; \
    rm -rf /root/*;

#Add User
RUN useradd -rm -d /home/docker -s /bin/bash -u 1002 docker

USER docker

ENV Selenium_UseHeadlessDriver=true

#Add oil script
COPY oil.py /

#add Dependencies
RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install --no-cache-dir paho-mqtt selenium

CMD ["python", "-u" , "/oil.py"]