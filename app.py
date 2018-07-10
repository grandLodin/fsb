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


def get_deck(deckId):
    user_id = connexion.request.headers["userId"]
    return deck_handler.get_deck(user_id, deckId)


def delete_deck(deckId):
    user_id = connexion.request.headers["userId"]
    if deck_handler.delete_deck(user_id, deckId):
        return 204
    else: 
        return 404


def update_deck(deckId, deck):
    return 200

def list_avatars():
    return 200

def create_avatar(avatar):
    return 201

def get_avatar(avatarId):
    return 200

def delete_avatar(avatarId):
    return 204

def update_avatar(avatarId, avatar):
    return 200

def list_pits():
    return 200

def create_pit(pit):
    return 201

def get_pit(pitId):
    return 200

def delete_pit(pitId):
    return 204

def update_pit(pitId, pit):
    return 200

def list_deployed_minions(pitId):
    return 200

def deploy_minion(pitId, minion):
    return 201

def list_deployed_avatars(pitId):
    return 200

def deploy_avatar(pitId, avatar):
    return 201



logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__)
app.add_api('swagger.yaml')
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app

if __name__ == '__main__':
    # run our standalone gevent server
    app.run(port=8080, server='gevent')
