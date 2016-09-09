#!/usr/bin/python3

from bottle import route, run
import redis
import json
from datetime import datetime

import definations


@route('/feed')
def get_feed():
    output = [item.decode('utf-8') for item in r.zrange(REDIS_SET, 0, -1)]
    feeds = json.dumps(output)
    return feeds


# Get feeds after a specific time
@route('/pfeed/<aftertime>')
def get_feed_after_score(aftertime):
    now = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S.%f")
    output = [item.decode('utf-8') for item in r.zrangebyscore(REDIS_SET, aftertime, now)]
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
