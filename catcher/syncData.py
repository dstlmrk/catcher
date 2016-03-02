#!/usr/bin/python
# coding=utf-8

import urllib2
import sys
from models import *
# import MySQLdb

# ID oddílu, Oddíl, ID hráče, Příjmení, Jméno
CALD_CLUBS       = "http://archiv.cald.cz/caldMembersRecord/public/report/teams"
CALD_CLUBS_COLS  = 5

CALD_ROSTERS     = "http://archiv.cald.cz/caldMembersRecord/public/report/rosters"
CALD_TOURNAMENTS = "http://archiv.cald.cz/caldMembersRecord/public/report/tournaments"

DBNAME     = 'catcher'
TABLE_CLUB = 'club'

# # db = MySQLdb.connect(host='localhost', user='', passwd='', db='catcher')

# # you must create a Cursor object. It will let
# #  you execute all the queries you need
# cur = db.cursor()

# # Use all the SQL you like
# cur.execute("SELECT * FROM YOUR_TABLE_NAME")

# # print all the first cell of all the rows
# for row in cur.fetchall():
#     print row[0]

# db.close()

def loadFile(url):
    try:
        response = urllib2.urlopen(url)
        html = response.read()
    except URLError:
        sys.exit("Check your internet connection")
    except IOError:
        sys.exit("Can't open file from %s", url)
    return html.splitlines()

def divideFile(lines):
    return (lines[0], lines[1:])

def checkNumberOfColumns(line, expectedNumber):
    if  len(line.split('\t')) != expectedNumber:
        sys.exit("File has unexpected format")
    return True

def getTeam(line):
    line = line.split('\t')
    # unique shortcut is ready for future edit
    shortcut = (line[0] + "X" + line[1])[0:3].upper()
    # (id club, club, unique shortcut)
    return (line[0], line[1], shortcut)

def getPlayer(line):
    line = line.split('\t')
    # (id club, id player, firstname, lastname)
    return (line[0], line[2], line[3], line[4])

# load cald clubs and their players
caldPlayers = loadFile(CALD_CLUBS)
firstLine, caldPlayers = divideFile(caldPlayers)
checkNumberOfColumns(firstLine, CALD_CLUBS_COLS)

clubs = set()
players = set()

for line in caldPlayers:
    clubs.add(getTeam(line))
    players.add(getPlayer(line))

# if club doesn't exist, it will add them
for club in clubs:
    db.execute_sql('INSERT IGNORE INTO %s.%s (cald_id,name,shortcut) VALUES (\'%s\', \'%s\', \'%s\');'
        % (DBNAME, TABLE_CLUB, club[0], club[1], club[2])
        )