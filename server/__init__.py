import argparse
import os
import ssl
import flask

from flask_oauthlib.client import OAuth
from server.libs.logger import configure_logging


def _parse_args():
    parser = argparse.ArgumentParser(
        usage='faf voting microservice'
    )
    parser.add_argument('-d', '--debug', action='store_true', help='enable flask debugging')

    return parser.parse_args()


def _parse_env_vars(args) -> dict:
    env_vars = {
        'port': os.environ.get('PORT', 5000),
        'base_url': os.environ['BASE_URL'],
        'faf_api': os.environ['FAF_API'],
        'secret_key': os.environ['SECRET_KEY'],
        'consumer_key': os.environ['CONSUMER_KEY'],
        'consumer_secret': os.environ['CONSUMER_SECRET'],
        'db_credentials': {
            'password': os.environ['MYSQL_ROOT_PASSWORD'],
            'db': os.environ['MYSQL_DATABASE'],
            'host': os.environ['MYSQL_HOSTNAME'],
            'user': os.environ['MYSQL_USER']
        }
    }
    env_vars.update(vars(args))

    return env_vars


def _configure_app(args: dict):
    app = flask.Flask(__name__, static_folder='dist')
    # oauth bug dirty fix
    os.environ['DEBUG'] = '1'

    # Setup global configs
    app.secret_key = args['secret_key']
    app.config['SESSION_TYPE'] = 'filesystem'

    return app


def _configure_oauth(args: dict):
    return OAuth().remote_app(
        'faforever',
        consumer_key=args['consumer_key'],
        consumer_secret=args['consumer_secret'],
        base_url=args['base_url'] + "/oauth/authorize",
        access_token_url=args['faf_api'] + "/oauth/token",
        request_token_params={"scope": "public_profile"}
    )


def _register_blueprints(app, args):
    base_url = args['base_url']

    from server.routes.index import Index
    index = Index()
    app.register_blueprint(index.build_blueprint(), url_prefix='/')

    from server.routes.oauth import OAuth
    oauth = OAuth(_configure_oauth(args), base_url)
    app.register_blueprint(oauth.build_blueprint(), url_prefix='/oauth')

    from server.routes.vote import Vote
    vote = Vote(base_url, args['faf_api'], args['db_credentials'])
    app.register_blueprint(vote.build_blueprint(), url_prefix='/vote')


def _monkey_patch():
    # TODO: monkey patch to disable https cert verification. This is insecure as it allows for a
    # MIM attack if the service is not making https requests within a local network
    ssl._create_default_https_context = ssl._create_unverified_context


def create_app():
    args = _parse_env_vars(_parse_args())
    app = _configure_app(args)
    _register_blueprints(app, args)
    _monkey_patch()
    configure_logging()

    return app, args
