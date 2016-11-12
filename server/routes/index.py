from flask import Blueprint
from server.abc.base_route import Route


class Index(Route):
    def build_blueprint(self):
        index = Blueprint('index', __name__)

        @index.route("/")
        def root():
            return index.send_static_file('views/index.html')

        return index
