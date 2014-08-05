from models import Player
import logging
from google.appengine.ext import ndb

def get_player_from_email(email):
  """Helper method to get the Player object corresponding to the given User.
  Creates a new Player object if one didn't exist already.
  """
  player = Player.get_by_id(email.lower()) # Something like this
  if not player:
    logging.info("Failed to find player by userid, creating new user")
    player = Player(id=email.lower())
    player.put()
  return player

def get_parent_key(user):
    return ndb.Key("Entity", user.email().lower())

