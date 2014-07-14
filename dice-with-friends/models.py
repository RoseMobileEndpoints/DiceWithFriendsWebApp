from google.appengine.ext import ndb
import logging

class Player(ndb.Model):
  """ Holder information for a player. """
  lowercase_email = ndb.StringProperty(required=True)
  display_name = ndb.StringProperty()
  create_time = ndb.DateTimeProperty(auto_now_add=True)
  last_update = ndb.DateTimeProperty(auto_now=True)

  def get_display_name(self):
    """Returns a suitable display name for use on the leaderboards."""
    if self.display_name:
      return self.display_name
    elif self.lowercase_email:
      return self.lowercase_email
    else:
      return ''

  @staticmethod
  def get_player_from_email(email):
    """Helper method to get the Player object corresponding to the given User.
    Creates a new Player object if one didn't exist already.
    """
    player = Player.query(Player.lowercase_email==email.lower()).get()
    if not player:
      logging.info("Failed to find player by userid, creating new user")
      player = Player(id=email.lower(), lowercase_email=email.lower())
      player.put()
    logging.info("Player: " + player.key.urlsafe())
    return player

class Game(ndb.Model):
    """ Dice with Friends game. """
    player1_key = ndb.KeyProperty(kind=Player)  # Created the game
    player2_key = ndb.KeyProperty(kind=Player)  # Invited to play in the game
    player1_scores = ndb.IntegerProperty(repeated=True)
    player2_scores = ndb.IntegerProperty(repeated=True)
    last_update_by_player1 = ndb.DateTimeProperty()
    last_update_by_player2 = ndb.DateTimeProperty()
    create_time = ndb.DateTimeProperty(auto_now_add=True)

    # Convenience fields (things that could be calculated from other data.
    rounds_completed = ndb.IntegerProperty(default=0)
    player1_score = ndb.IntegerProperty()  # Score after rounds_completed
    player2_score = ndb.IntegerProperty()  # Score after rounds_completed
    winner = ndb.KeyProperty(kind=Player)


