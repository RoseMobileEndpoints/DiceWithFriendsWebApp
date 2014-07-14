
from google.appengine.api import users
import webapp2
import logging

import main
import models
import time


class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            template = main.jinja_env.get_template("templates/not_logged_in.html")
            self.response.out.write(template.render({'login_url': users.create_login_url("/")}))
        else:
            player = models.Player.get_player_from_email(user.email())
            if not player.display_name or not len(player.display_name) > 0:
              template = main.jinja_env.get_template("templates/set_display_name.html")
              self.response.out.write(template.render({'logout_url': users.create_logout_url("/")}))
            else:
              template = main.jinja_env.get_template("templates/main.html")
              self.response.out.write(template.render({'player': player,
                                                     'logout_url': users.create_logout_url("/")}))

    def post(self):
        """ Used to set the display name for a player. """
        user = users.get_current_user()
        if not user:
          raise Exception("Missing user.")
        player = models.Player.get_player_from_email(user.email())
        player.display_name = self.request.get('display_name')
        player.put()
        time.sleep(0.5) # Hack.  Didn't want to implement a Parent key to get strong consistency.
        self.redirect(self.request.referer)
