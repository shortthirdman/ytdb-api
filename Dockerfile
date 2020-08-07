FROM python:3.7.8-slim-buster
LABEL MAINTAINER="Swetank Mohanty (shortthirdman) <swetank.mohanty@outlook.com>"
ENV DBX_ACCESS_TOKEN '49K0FmjttHkAAAAAAAAE8-4JSEo3slC1OSIJUKeJsxK7STIHH9zRhgzsol9mgJ-0'
ENV DBX_APP_KEY 'dfqk8tuuc2h0sr0'
ENV DBX_APP_SECRET '8boa9h23cgiripc'
ENV DBX_CLIENT_ID 'dropbox/youtube'
RUN python --version
RUN pip --version
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ytdb-api.py ./
ENTRYPOINT [ "python", "./ytdb-api.py" ]