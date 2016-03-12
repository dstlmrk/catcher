#!/usr/bin/python
# coding=utf-8

import urllib2
import sys
import config

import models

class ImportFile(object):
    def __init__(self, url, expectedCols, delimiter):
        self.url       = url
        self.delimiter = delimiter
        self.html      = self._loadFile(self.url)
        self.body      = self._getBody(self.html, expectedCols, delimiter)

    def _loadFile(self, url):
        try:
            response = urllib2.urlopen(self.url)
            html = response.read()
        except urllib2.URLError:
            # TODO: doplnit vyjimku
            sys.exit("Can't connect to %s", self.url)
        except IOError:
            # TODO: doplnit vyjimku
            sys.exit("Can't open file from %s", self.url)
        return html

    def _cutHeader(self, html):
        lines  = html.splitlines()
        header = lines[0]
        body   = lines[1:]
        return (header, body)

    def _getBody(self, html, expectedCols, delimiter):
        header, body = self._cutHeader(html)
        fileCols = header.split(delimiter)
        if fileCols != expectedCols:
            # TODO: doplnit vyjimku
            sys.exit("File has unexpected format")
            # raise IOError("File has unexpected format")
        return body

class ImportClubsAndPlayers(ImportFile):
    def __init__(self, *args):
        super(ImportClubsAndPlayers, self).__init__(*args)

    def _getTeam(self, line):
        line = line.split(self.delimiter)
        # TODO: dodelat naprostou kontrolu nad tim, ze pujde o unikatni hodnotu
        # unique shortcut is ready for future edit
        shortcut = (line[0] + "X" + line[1])[0:3].upper()
        # (id club, club, unique shortcut)
        return (line[0], line[1], shortcut)

    def _getPlayer(self, line):
        line = line.split(self.delimiter)
        # (id club, id player, firstname, lastname)
        return (line[0], line[2], line[3], line[4])

    def _getRelation(self, line):
        line = line.split(self.delimiter)
        # (id club, id player)
        return (line[0], line[2])


    def importClubs(self):
        clubs = set()
        for line in self.body:
            clubs.add(self._getTeam(line))
        
        # if club doesn't exist, it will add them
        newClubs = 0
        for club in clubs:
            try:
                models.db.execute_sql(
                    'INSERT INTO %s.%s (cald_id, name, shortcut) VALUES (%d, \'%s\', \'%s\');'
                    % (models.DBNAME, models.TABLE_CLUB, int(club[0]), club[1], club[2])
                    )
            except models.pw.IntegrityError as e:
                # IGNORE = duplicate rows will be not inserted
                pass
            else:
                newClubs += 1
        return newClubs

    def importPlayers(self):
        players = set()
        for line in self.body:
            players.add(self._getPlayer(line))

        newPlayers = 0
        transfers  = 0

        for player in players:
            cald_club_id = int(player[0])
            cald_id      = int(player[1])
            lastname     = player[2]
            firstname    = player[3]

            try:
                models.Player.insert(
                    cald_club_id = cald_club_id,
                    cald_id      = cald_id,
                    lastname     = lastname,
                    firstname    = firstname
                    ).execute()
            except models.pw.IntegrityError as ex:
                qr = models.Player\
                    .update(cald_club_id = cald_club_id)\
                    .where(models.Player.cald_id==cald_id)\
                    .execute()
                transfers += int(qr)
            else:
                newPlayers += 1

            try:
                player = models.Player.get(cald_id=cald_id)
                club = models.Club.get(cald_id=cald_club_id)
                models.ClubHasPlayer.insert(player=player, club=club).execute()
            except models.MySQLModel.DoesNotExist as ex:
                raise models.MySQLModel.DoesNotExist(ex)
                continue
            except models.pw.IntegrityError as ex:
                # IGNORE = duplicate rows will be not inserted
                pass

        return newPlayers, transfers

    def importClubsAndPlayers(self):
        newClubs               = self.importClubs()
        newPlayers, transfers  = self.importPlayers()
        print("Imported:\n"
            + "- %d new clubs\n"   % (newClubs)
            + "- %d new players\n" % (newPlayers)
            + "- %d transfers"     % (transfers)
            )

print "1. Started"

clubs = ImportClubsAndPlayers(
    config.cald.clubs['url'],
    config.cald.clubs['columns'],
    config.cald.clubs['delimiter'],
    )

print "2. Loaded file"

clubs.importClubsAndPlayers()

print "3. Imported clubs and players"