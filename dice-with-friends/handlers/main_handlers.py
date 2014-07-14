
from google.appengine.api import users
import webapp2
import logging

import main
import models
import time

class BaseHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not user:
      template = main.jinja_env.get_template("templates/home.html")
      self.response.out.write(template.render({'login_url': users.create_login_url(self.request.referer)}))
    else:
      player = models.Player.get_player_from_email(user.email())
      if not player.display_name or not len(player.display_name) > 0:
        self.redirect("/set_display_name")
      else:
        values = {'player': player, 'logout_url': users.create_logout_url("/")}
        self.update_values(player, values)
        template = main.jinja_env.get_template(self.get_template())
        self.response.out.write(template.render(values))

  def update_values(self, player, base_values):
    return


class HomeHandler(BaseHandler):
  def get_template(self):
    return "templates/home.html"

  def update_values(self, player, base_values):
    return


class SetDisplayNameHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            template = main.jinja_env.get_template("templates/home.html")
            self.response.out.write(template.render({'login_url': users.create_login_url("/")}))
        else:
            player = models.Player.get_player_from_email(user.email())
            template = main.jinja_env.get_template("templates/set_display_name.html")
            self.response.out.write(template.render({'player': player, 'logout_url': users.create_logout_url("/")}))

    def post(self):
        """ Used to set the display name for a player. """
        user = users.get_current_user()
        if not user:
          raise Exception("Missing user.")
        player = models.Player.get_player_from_email(user.email())
        player.display_name = self.request.get('display_name')
        player.put()
        time.sleep(0.5)  # Hack.  Didn't want to implement a Parent key to get strong consistency.
        self.redirect("/")
