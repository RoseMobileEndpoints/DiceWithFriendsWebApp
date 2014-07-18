from google.appengine.ext import ndb

from endpoints_proto_datastore.ndb.model import EndpointsModel


class Player(EndpointsModel):
  """ Holder information for a player. """
  _message_fields_schema = ("id", "display_name", "create_time")
  display_name = ndb.StringProperty()

  def get_name(self):
    """Returns a suitable display name for use on the leaderboards."""
    if self.display_name:
      return self.display_name
    return self.key.string_id()

class Game(EndpointsModel):
  """ Dice with Friends game. """
  _message_fields_schema = ("entityKey", "creator_key", "invitee_key", "creator_scores", "invitee_scores", 
                            "last_touch_date_time")
  creator_key = ndb.KeyProperty(kind=Player)
  invitee_key = ndb.KeyProperty(kind=Player)
  creator_scores = ndb.IntegerProperty(repeated=True)
  invitee_scores = ndb.IntegerProperty(repeated=True)
  last_touch_date_time = ndb.DateTimeProperty(auto_now=True)
  is_complete = ndb.BooleanProperty()