from google.appengine.ext import ndb

class Player(ndb.Model):
  """ Holder information for a player. """
  display_name = ndb.StringProperty()
  create_time = ndb.DateTimeProperty(auto_now_add=True)

  def get_name(self):
    """Returns a suitable display name for use on the leaderboards."""
    if self.display_name:
      return self.display_name
    return self.key.string_id()

class Game(ndb.Model):
  """ Dice with Friends game. """
  creator_key = ndb.KeyProperty(kind=Player)
  invitee_key = ndb.KeyProperty(kind=Player)
  creator_scores = ndb.IntegerProperty(repeated=True)
  invitee_scores = ndb.IntegerProperty(repeated=True)
  last_update_by_creator = ndb.DateTimeProperty()
  last_update_by_invitee = ndb.DateTimeProperty()
  create_time = ndb.DateTimeProperty(auto_now_add=True)
