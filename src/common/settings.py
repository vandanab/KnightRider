'''
Created on Nov 21, 2012

@author: vandana
settings used by the common functions
'''

DB_SERVER='localhost'
DB_PORT=27017
CRAWLER_DB_NAME='pinterest_crawler'

#files hierarchy year/month/day/starttime.json

DATADIR = "/home/vandana/workspace/KnightRider/data/%s/"
PINS_DIR = DATADIR % "pins"
USERS_DIR = DATADIR % "users"