from flask import session, redirect, Blueprint, jsonify
from server.abc.base_route import Route


class OAuth(Route):
    def __init__(self, oauth_service, base_url):
        self.oauth = oauth_service
        self.redirect_url = base_url + "/auth"

    def build_blueprint(self):
        oauth = Blueprint('oauth', __name__)

        @oauth.route("/login")
        def login():
            return self.oauth.authorize(callback=self.redirect_url)

        @oauth.route('/auth', methods=["GET", "POST"])
        def auth():
            resp = self.oauth.authorized_response()
            if resp is None:
                return jsonify({'error': 'Token not received'}), 401
            token = resp["access_token"]
            session['token'] = token

            return redirect("/vote")

        return oauth
