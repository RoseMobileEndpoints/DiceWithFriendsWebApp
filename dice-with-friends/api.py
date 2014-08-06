'''
Created on Jul 16, 2014

@author: Matt Boutell and Dave Fisher
'''

import logging

import endpoints
from google.appengine.ext import ndb
import protorpc

import main
from models import Player, Game
from utils import player_utils, game_utils


# For authentication
WEB_CLIENT_ID = ""
ANDROID_CLIENT_ID_DAVE = ""
ANDROID_CLIENT_ID_MATT = ""

IOS_CLIENT_ID = ""

@endpoints.api(name="dicewithfriends", version="v1", description="Dice with Friends API",
               hostname="dice-with-friends.appspot.com", audiences=[WEB_CLIENT_ID],
               allowed_client_ids=[endpoints.API_EXPLORER_CLIENT_ID, WEB_CLIENT_ID, ANDROID_CLIENT_ID_DAVE, ANDROID_CLIENT_ID_MATT, IOS_CLIENT_ID])
class DiceWithFriendsApi(protorpc.remote.Service):

  """
    Player insert
    Game:
      insert
      delete
      queryWaitingForMe:         'my' score < 10K & rounds < rounds where opponent hit 10K  
      queryWaitingOnlyForOpponent  score >= 10K & opp score < 10 K & opponent round < round where I hit 10K
      queryCompletedGames      (use boolean)
    """

  # Insert methods
  @Player.method(user_required= True, name="player.insert", path="player/insert", http_method="POST")
  def player_insert(self, player):
    """ Add or update a player for the given user """
    
    # get_player_from_email will create a new player if none exists
    player_with_parent = player_utils.get_player_from_email(endpoints.get_current_user().email())
    player_with_parent.display_name = player.display_name
    player_with_parent.put()
    return player_with_parent

  @Game.method(user_required= True, name="game.insert", path="game/insert", http_method="POST")
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
    # Required to order by key first to do a multi (OR) filter.
    query = query.order(Game._key).filter(ndb.OR(Game.creator_key == player.key, Game.invitee_key == player.key))
    return query

 
#     @Assignment.query_method(user_required=True, query_fields=("limit", "pageToken"),
#                              name="assignment.list", path="assignment/list", http_method="GET")
#     def assignment_list(self, query):
#         """ List all the assignments owned by the user """
#         user = endpoints.get_current_user()
#         assignments = Assignment.query(ancestor=main.get_parent_key(user)).order(Assignment.name)
#         return assignments
# 
#     @GradeEntry.query_method(user_required=True, query_fields=("limit", "order", "pageToken", "assignment_key"),
#                              name="gradeentry.list", path="gradeentry/list/{assignment_key}", http_method="GET")
#     def gradeentry_list(self, query):
#         """ List all the grade entries for the given assignment key """
#         return query
# 
# 
#     # Delete methods
#     @Assignment.method(user_required= True, request_fields = ("entityKey",),
#                        name="assignment.delete", path="assignment/delete/{entityKey}", http_method="DELETE")
#     def assignment_delete(self, assignment):
#         """ Delete the assignment with the given key, plus all the associated grade entries """
#         if not assignment.from_datastore:
#             raise endpoints.NotFoundException("No assignment found for the given key")
#         children = GradeEntry.query(ancestor=assignment.key)
#         for grade_entry in children:
#             grade_entry.key.delete()
#         assignment.key.delete()
#         return Assignment(name="deleted")
# 
#     @GradeEntry.method(user_required= True, request_fields = ("entityKey",),
#                        name="gradeentry.delete", path="gradeentry/delete/{entityKey}", http_method="DELETE")
#     def gradeentry_delete(self, grade_entry):
#         """ Delete the grade entry with the given key """
#         if not grade_entry.from_datastore:
#             raise endpoints.NotFoundException("No grade entry found for the given key")
#         grade_entry.key.delete()
#         return GradeEntry()


app = endpoints.api_server([DiceWithFriendsApi], restricted=False)


