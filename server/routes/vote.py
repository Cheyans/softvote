import server.libs.database as database
import requests
from flask import session, request, Blueprint, jsonify
from server.abc.base_route import Route


class Vote(Route):
    def __init__(self, base_url, api, db_credentials):
        self.base_url = base_url
        self.api = api
        self.db_credentials = db_credentials

    def build_blueprint(self):
        vote = Blueprint('vote', __name__)

        @vote.route('/<question_id>/<answer_id>', methods=["POST"])
        def cast_vote(question_id, answer_id):
            token = session.get("token")
            if not token:
                return jsonify({'error': 'Token not received'}), 401

            conn = database.connect(**self.db_credentials)
            response = requests.get(self.api + "/players/me", headers={"Authorization": "Bearer " + token})
            voter_id = response.json()["data"]["id"]
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO votes(voter_id, question_id, answer_id, ip) VALUES(%s, %s, %s, %s)",
                               (voter_id, question_id, answer_id, request.remote_addr))
            conn.commit()
            return jsonify({'message': 'Success'})

        @vote.route('/<question_id>', methods=["GET"])
        def get_answers(question_id):
            conn = database.connect(**self.db_credentials)
            with conn.cursor() as cursor:
                cursor.execute("SELECT answer, display_order FROM answers WHERE question_id=%s", (question_id,))
                answers = cursor.fetchall()
            return jsonify(answers)

        return vote
