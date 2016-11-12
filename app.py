#!/usr/bin/env python
from server import create_app
from server.libs.logger import log

if __name__ == '__main__':
    app, args = create_app()
    log().info('Starting server')
    app.run(host='0.0.0.0', port=int(args['port']), debug=bool(args['debug']))
