from bottle import route, run
import configparser
import os
import redis

settings = configparser.ConfigParser()
BASEDIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = os.path.join(BASEDIR + '/config.ini')
settings.read(CONFIG_FILE)

REDIS_SET = settings.get('Production', 'redis_set')
REDIS_HOST = settings.get('Production', 'redis_host')


@route('/feed')
def get_feed():
    output = ''
    for item in r.zrange(REDIS_SET, 0, -1):
        output += item.decode('utf-8')
        output += '<br/>'
    return output


r = redis.Redis(host=REDIS_HOST, port="6379")
run(host='localhost', port=8888, debug=True, reloader=True)
