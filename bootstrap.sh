#!/bin/bash

sed -i.bak s/ftp\.us\.debian\.org/ftp\.se\.debian\.org/g /etc/apt/sources.list

apt-get update
apt-get upgrade

apt-get install python3 python3-pip redis-server

pip-3.2 install django django-ipware
# pip-3.2 install django-websocket-redis
pip-3.2 install https://github.com/mbrrg/django-websocket-redis/zipball/python3-support


#apt-get install build-essential python-dev
