Pull facebook group feed and gives feed in most-recent order

Requires: 
    Redis python wrapper: https://github.com/chester89/redis-py.git:zadd-options


Consists of two application: 
    * fbconnector: Pulls data from facebook and updates to redis
    * web_app: Pulls data from redis and send it back to user 
