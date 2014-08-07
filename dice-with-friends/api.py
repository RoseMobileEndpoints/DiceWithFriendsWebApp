'''
Created on Jul 16, 2014

@author: Matt Boutell and Dave Fisher
'''

import endpoints
from google.appengine.ext import ndb
import protorpc

from models import Player, Game
from utils import player_utils


# For authentication
WEB_CLIENT_ID = ""
ANDROID_CLIENT_ID_DAVE = ""
ANDROID_CLIENT_ID_MATT = ""

IOS_CLIENT_ID = ""

@endpoints.api(name="dicewithfriends", version="v1", description="Dice with Friends API",
               hostname="dice-with-friends.appspot.com", audiences=[WEB_CLIENT_ID],
               allowed_client_ids=[endpoints.API_EXPLORER_CLIENT_ID, WEB_CLIENT_ID, ANDROID_CLIENT_ID_DAVE, ANDROID_CLIENT_ID_MATT, IOS_CLIENT_ID])
class DiceWithFriendsApi(protorpc.remote.Service):

  # Single getters 
  @Player.method(user_required=True, request_fields=(), name="player.get", path="player/get", http_method="GET")
  def player_get(self, player):
    """ Returns the Player for the given user """
    return player_utils.get_player_from_email(endpoints.get_current_user().email())

  @Player.method(user_required=True, request_fields=("entityKey",), response_fields=("display_name",), name="player.getname",
                 path="player/getname/{entityKey}", http_method="GET")
  def player_get_name(self, player):
    """ Returns the Player for the given entityKey with the best name available in the display name. """
    if not player.from_datastore:
      raise endpoints.NotFoundException('Player not found.')
    player.display_name = player.get_name()
    return player

  # Insert methods
  @Player.method(user_required=True, name="player.insert", path="player/insert", http_method="POST")
  def player_insert(self, player):
    """ Add or update a player for the given user """

    # get_player_from_email will create a new player if none exists
    player_with_parent = player_utils.get_player_from_email(endpoints.get_current_user().email())
    player_with_parent.display_name = player.display_name
    player_with_parent.put()
    return player_with_parent

  @Game.method(user_required=True, name="game.insert", path="game/insert", http_method="POST")
  def game_insert(self, game):
    """ Add or update a game """
    if game.from_datastore:
      game_with_parent = game
    else:
      creator = endpoints.get_current_user()
      player_for_creator = player_utils.get_player_from_email(creator.email())
      if game.invitee_email:
        invited_player_key = player_utils.get_player_from_email(game.invitee_email).key
      else:
        invited_player_key = None

      game_with_parent = Game(parent = player_for_creator.key,
                              creator_key = player_for_creator.key,
                              invitee_key = invited_player_key,
                              is_solo = not invited_player_key
                              )
      game_with_parent.put()
      return game_with_parent

  # List methods
  @Game.query_method(user_required=True, query_fields=("is_solo", "is_complete", "limit", "order", "pageToken"),
                          name="game.list", path="game/list", http_method="GET")
  def game_list(self, query):
    """ List all the games for this user """
    player = player_utils.get_player_from_email(endpoints.get_current_user().email())
    # Required to order by key first when filter uses IN, OR, or !=, due to query cursor created for 
    # page tokens that endpoints proto datastore implements after this method completes.
    query = query.order(Game.key).filter(ndb.OR(Game.creator_key == player.key, Game.invitee_key == player.key))
    return query

  # Delete methods
  @Game.method(user_required=True, request_fields = ("entityKey",), response_fields = (),
               name="game.delete", path="game/delete/{entityKey}", http_method="DELETE")
  def game_delete(self, game):
        """ Delete the game with the given key """
        if not game.from_datastore:
            raise endpoints.NotFoundException("No game found for the given key")
        game.key.delete()
        return Game()

app = endpoints.api_server([DiceWithFriendsApi], restricted=False)
