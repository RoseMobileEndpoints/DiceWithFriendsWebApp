from google.appengine.ext import ndb
import logging

class Player(ndb.Model):
  """ Holder information for a player. """
  lowercase_email = ndb.StringProperty(required=True)
  display_name = ndb.StringProperty()
  create_time = ndb.DateTimeProperty(auto_now_add=True)
  last_update = ndb.DateTimeProperty(auto_now=True)

  def get_name(self):
    """Returns a suitable display name for use on the leaderboards."""
    if self.display_name:
      return self.display_name
    elif self.lowercase_email:
      return self.lowercase_email
    else:
      return ''


class Game(ndb.Model):
  """ Dice with Friends game. """
  # Note the player that created this
  creator_player_key = ndb.KeyProperty(kind=Player)  # Created the game (Duplicate of the parent key!)
  invited_player_key = ndb.KeyProperty(kind=Player)  # Invited to play in the game
  creator_scores = ndb.IntegerProperty(repeated=True)
  invited_player_scores = ndb.IntegerProperty(repeated=True)
  last_update_by_creator = ndb.DateTimeProperty()
  last_update_by_invited_player = ndb.DateTimeProperty()
  create_time = ndb.DateTimeProperty(auto_now_add=True)

