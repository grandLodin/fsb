#!/usr/bin/env python3
import connexion
import datetime
import logging

from connexion import NoContent


def get_decks():
    id = connexion.request.headers["userId"]
    print(id)
    return [{"id": id}]

def create_deck(deck):
    print(deck)
    return "Created", 201

def delete_deck(deckId):
    print("Deleted deck " + deckId)
    return  204

logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__)
app.add_api('swagger.yaml')
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app

if __name__ == '__main__':
    # run our standalone gevent server
    app.run(port=8080, server='gevent')