FROM mcr.microsoft.com/playwright/python:v1.30.0-focal
WORKDIR /app

ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
ENV PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
ENV DEBUG=pw:browser,pw:api

COPY requirements.txt /app

RUN pip install -r /app/requirements.txt
RUN python3 -m playwright install
RUN #python3 -m playwright install chrome
RUN apt-get update && apt-get install wget unzip zip -y
RUN wget --no-verbose -O /tmp/chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_104.0.5112.101-1_amd64.deb \
  && apt install -y /tmp/chrome.deb \
  && rm /tmp/chrome.deb

COPY . /app
RUN ["chmod", "+x", "./ci/run.sh"]
ENTRYPOINT ["./ci/run.sh"]
