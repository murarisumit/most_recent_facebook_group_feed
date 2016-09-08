#!/usr/bin/python3

from bottle import route, run
import redis
import json

import definations


@route('/feed')
def get_feed():
    output = []
    for item in r.zrange(REDIS_SET, 0, -1):
        output.append(item.decode('utf-8'))
    feeds = json.dumps(output)
    return feeds


if __name__ == "__main__":
    settings = definations.settings
    ENV = definations.ENV
    REDIS_SET = settings.get(ENV, 'redis_set')
    REDIS_HOST = settings.get(ENV, 'redis_host')
    DEBUG = settings.get(ENV, 'DEBUG')
    PORT = settings.get(ENV, 'PORT')
    RELOADER = settings.get(ENV, 'RELOADER')

    r = redis.Redis(host=REDIS_HOST, port="6379")
    run(host='0.0.0.0', server='gunicorn', workers=4,
        port=PORT, debug=DEBUG, reloader=RELOADER
        )
