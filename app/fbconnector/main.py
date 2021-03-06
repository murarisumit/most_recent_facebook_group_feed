#!/usr/bin/python3
import requests
import json
import redis
from datetime import datetime
import time
import sys
import definations


def update_feed():
    try:
        feed = requests.get(base_url + '/v2.7/' + GROUP_ID + '?fields=feed.limit(20).since(60)', params={'access_token': access_token})
    except:
        print("Unexpected error:", sys.exc_info()[0])
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


if __name__ == "__main__":
    print("== Program started ==")
    settings = definations.settings
    ENV = definations.ENV

    base_url = settings.get(ENV, 'base_url')
    CLIENT_ID = settings.get(ENV, 'client_id')
    CLIENT_SECRET = settings.get(ENV, 'client_secret')
    GROUP_ID = settings.get(ENV, 'group_id')
    REDIS_HOST = settings.get(ENV, 'redis_host')
    REDIS_SET = settings.get(ENV, 'redis_set')

    r = redis.Redis(host=REDIS_HOST, port="6379")
    access_token = get_access_token()
    while 1:
        update_feed()
        print(" == Going to sleep == ")
        time.sleep(20)
        print(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S.%f"))
