import requests
import json
import redis
from datetime import datetime
import time
import configparser
import os


settings = configparser.ConfigParser()
BASEDIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = os.path.join(BASEDIR + '/config.ini')
print(CONFIG_FILE)
settings.read(CONFIG_FILE)
base_url = settings.get('Production', 'BASE_URL')
CLIENT_ID = settings.get('Production', 'CLIENT_ID')
CLIENT_SECRET = settings.get('Production', 'CLIENT_SECRET')
GROUP_ID = settings.get('Production', 'GROUP_ID')
REDIS_SET = settings.get('Production', 'redis_set')


def update_feed():
    access_token = get_access_token()
    feed = requests.get(base_url + '/v2.7/' + GROUP_ID + '?fields=feed.limit(20).since(60)', params={'access_token': access_token})
    parsed_json = json.loads(feed.text)
    ids = get_ids(parsed_json)
    return ids


def get_access_token():
    r = requests.get(base_url + '/oauth/access_token?grant_type=client_credentials&client_id=' + CLIENT_ID + '&client_secret=' + CLIENT_SECRET)
    access_token = r.text.split('=')[1]
    return access_token


def get_ids(parsed_json):
    output = ''
    for item in parsed_json['feed']['data']:
        print(item['id'])
        store_id_to_redis(item['id'])
    return output


def store_id_to_redis(key):
    timestamp = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S.%f")
    r.zaddnx(REDIS_SET, key, timestamp)


r = redis.Redis(host="localhost", port="6379")
print("== Program started ==")
while 1:
    update_feed()
    print(" == Going to sleep == ")
    time.sleep(20)
    print(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S.%f"))
