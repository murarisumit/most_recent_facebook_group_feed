#!/usr/bin/python3

from bottle import route, run
import configparser
import os
import redis
import json


@route('/feed')
def get_feed():
    output = []
    for item in r.zrange(REDIS_SET, 0, -1):
        output.append(item.decode('utf-8'))
    feeds = json.dumps(output)
    return feeds


if __name__ == "__main__":
    ENV = os.environ["ENVIRONMENT"]
    settings = configparser.ConfigParser()
    BASEDIR = os.path.dirname(os.path.realpath(__file__))
    CONFIG_FILE = os.path.join(BASEDIR + '/' + ENV + '_config.ini')
    settings.read(CONFIG_FILE)

    REDIS_SET = settings.get(ENV, 'redis_set')
    REDIS_HOST = settings.get(ENV, 'redis_host')
    DEBUG = settings.get(ENV, 'DEBUG')
    PORT = settings.get(ENV, 'PORT')
    RELOADER = settings.get(ENV, 'RELOADER')

    r = redis.Redis(host=REDIS_HOST, port="6379")
    run(host='localhost', port=PORT, debug=DEBUG, reloader=RELOADER)
