from models import Player
import logging
from google.appengine.ext import ndb

def get_player_from_email(email):
  """Helper method to get the Player object corresponding to the given User.
  Creates a new Player object if one didn't exist already.
  """
  player = Player.get_by_id(email.lower(), parent=get_parent_key_from_email(email)) 
  if not player:
    logging.info("Failed to find player by id, creating new user")
    player = Player(parent=get_parent_key_from_email(email), id=email.lower())
    player.put()
  return player


def get_parent_key(user):
    return get_parent_key_from_email(user.email())

def get_parent_key_from_email(email):
    return ndb.Key("Entity", email.lower())
