#!/usr/bin/env python3
import connexion
import logging
from client.main.deckhandler import DeckHandler

deck_handler = DeckHandler()


def list_decks():
    user_id = connexion.request.headers["userId"]
    return deck_handler.list_decks(user_id)
    

def create_deck(deck):
    user_id = connexion.request.headers["userId"]
    return deck_handler.create_deck(user_id, deck)


def get_deck(deck_id):
    user_id = connexion.request.headers["userId"]
    return deck_handler.get_deck(user_id, deck_id)


def delete_deck(deck_id):
    user_id = connexion.request.headers["userId"]
    if deck_handler.delete_deck(user_id, deck_id):
        return 204
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