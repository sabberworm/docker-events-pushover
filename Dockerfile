FROM python:3-alpine

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip install --upgrade pip "setuptools<58"

RUN pip install --no-cache-dir -r requirements.txt && \
  rm /usr/src/app/requirements.txt

CMD [ "/usr/local/bin/python", "-m", "docker-events-pushover" ]
