#!/usr/bin/env python3
import connexion
import datetime
import logging

from connexion import NoContent
from client.main.deckhandler import DeckHandler

deckhandler = DeckHandler()


def get_decks():
    userId = connexion.request.headers["userId"]
    return deckhandler.get_decks(userId)
    

def create_deck(deck):
    userId = connexion.request.headers["userId"]
    return deckhandler.create_deck(userId, deck)


def delete_deck(deckId):
    userId = connexion.request.headers["userId"]
    if deckhandler.delete_deck(userId, deckId):
        return  204
    else: 
        return 404

logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__)
app.add_api('swagger.yaml')
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app

if __name__ == '__main__':
    # run our standalone gevent server
    app.run(port=8080, server='gevent')