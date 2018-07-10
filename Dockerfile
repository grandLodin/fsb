FROM python:3
WORKDIR /usr/src/app
RUN pip install --no-cache-dir gevent connexion pick
COPY . .
CMD [ "python", "./app.py" ]