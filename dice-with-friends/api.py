'''
Created on Jul 16, 2014

@author: Matt Boutell and Dave Fisher
'''

import endpoints
import main
from models import Player, Game
import protorpc
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
    if player.from_datastore:
      player_with_parent = player
    else:
      user = endpoints.get_current_user()
      player_with_parent = Player(parent = player_utils.get_parent_key(user),
                                                id = user.email().lower(),
                                                display_name = player.display_name)
    player_with_parent.put()
    return player_with_parent

    @GradeEntry.method(user_required= True, name="gradeentry.insert", path="gradeentry/insert", http_method="POST")
    def gradeentry_insert(self, grade_entry):
        """ Add or update a grade entry for an assignment """
        if grade_entry.from_datastore:
            grade_entry_with_parent = grade_entry
        else:
            student = grade_entry.student_key.get()
            grade_entry_with_parent = GradeEntry(parent = grade_entry.assignment_key,
                                                 id = student.rose_username,
                                                 score = grade_entry.score,
                                                 student_key = grade_entry.student_key,
                                                 assignment_key = grade_entry.assignment_key)
        grade_entry_with_parent.put()
        return grade_entry_with_parent

    # List methods
    @Student.query_method(user_required=True, query_fields=("limit", "order", "pageToken"),
                          name="student.list", path="student/list", http_method="GET")
    def student_list(self, query):
        """ List all the students for this user """
        user = endpoints.get_current_user()
        students = Student.query(ancestor=main.get_parent_key(user)).order(Student.rose_username)
        return students

    @Assignment.query_method(user_required=True, query_fields=("limit", "pageToken"),
                             name="assignment.list", path="assignment/list", http_method="GET")
    def assignment_list(self, query):
        """ List all the assignments owned by the user """
        user = endpoints.get_current_user()
        assignments = Assignment.query(ancestor=main.get_parent_key(user)).order(Assignment.name)
        return assignments

    @GradeEntry.query_method(user_required=True, query_fields=("limit", "order", "pageToken", "assignment_key"),
                             name="gradeentry.list", path="gradeentry/list/{assignment_key}", http_method="GET")
    def gradeentry_list(self, query):
        """ List all the grade entries for the given assignment key """
        return query


    # Delete methods
    @Assignment.method(user_required= True, request_fields = ("entityKey",),
                       name="assignment.delete", path="assignment/delete/{entityKey}", http_method="DELETE")
    def assignment_delete(self, assignment):
        """ Delete the assignment with the given key, plus all the associated grade entries """
        if not assignment.from_datastore:
            raise endpoints.NotFoundException("No assignment found for the given key")
        children = GradeEntry.query(ancestor=assignment.key)
        for grade_entry in children:
            grade_entry.key.delete()
        assignment.key.delete()
        return Assignment(name="deleted")

    @GradeEntry.method(user_required= True, request_fields = ("entityKey",),
                       name="gradeentry.delete", path="gradeentry/delete/{entityKey}", http_method="DELETE")
    def gradeentry_delete(self, grade_entry):
        """ Delete the grade entry with the given key """
        if not grade_entry.from_datastore:
            raise endpoints.NotFoundException("No grade entry found for the given key")
        grade_entry.key.delete()
        return GradeEntry()


app = endpoints.api_server([GradeRecorderApi], restricted=False)


