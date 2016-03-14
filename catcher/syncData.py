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
            print("File is downloaded")
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
        # (id player, firstname, lastname)
        return (line[2], line[3], line[4])

    def _getRelation(self, line):
        line = line.split(self.delimiter)
        # (id club, id player)
        return (line[0], line[2])

    def _importClubs(self):
        '''If clubs don't exist, it will add them'''
        clubs = set()
        for line in self.body:
            clubs.add(self._getTeam(line))
    
        newClubs = 0
        for club in clubs:
            caldId   = int(club[0])
            name     = club[1]
            shortcut = club[2]

            try:
                models.Club.insert(
                    caldId   = caldId,
                    name     = name,
                    shortcut = shortcut
                    ).execute()
            except models.pw.IntegrityError as e:
                # duplicate rows will be not inserted
                pass
            else:
                newClubs += 1
        return newClubs

    def _importPlayers(self):
        '''If players don't exist, it will add them'''
        players = set()
        for line in self.body:
            players.add(self._getPlayer(line))

        newPlayers = 0

        for player in players:
            caldId    = int(player[0])
            lastname  = player[1]
            firstname = player[2]

            try:
                models.Player.insert(
                    caldId    = caldId,
                    lastname  = lastname,
                    firstname = firstname
                    ).execute()
            except models.pw.IntegrityError as ex:
                # duplicate rows will be not inserted
                pass
            else:
                newPlayers += 1


        return newPlayers

    def _importRelations(self):
        ''''''
        relations = set()
        for line in self.body:
            relations.add(self._getRelation(line))

        newRelations = 0

        for relation in relations:
            clubCaldId   = int(relation[0])
            playerCaldId = int(relation[1])

            try:
                club = models.Club.get(caldId=clubCaldId)
                player = models.Player.get(caldId=playerCaldId)
            except models.Club.DoesNotExist as ex:
                print("Club %d (cald id) doesn't exist" % (clubCaldId))
                continue
            except models.Player.DoesNotExist as ex:
                print("Player %d (cald id) doesn't exist" % (playerCaldId))
                continue

            try:
                # create new relation
                models.ClubHasPlayer.insert(
                    club         = club,
                    player       = player,
                    caldRelation = False
                    ).execute()
            except models.pw.IntegrityError as ex:
                # if exists, ignore it
                pass

            clubHasPlayer = models.ClubHasPlayer.get(club=club,player=player)
            if not clubHasPlayer.caldRelation:
                # somewhere exists old relation
                models.ClubHasPlayer.update(
                    caldRelation = False
                ).where(
                    player       = player,
                    caldRelation = True
                ).execute()
                # set new relation
                qr = models.ClubHasPlayer.update(
                    caldRelation = True
                ).where(
                    club         = club,
                    player       = player
                ).execute()
                newRelations += int(qr)

        return newRelations

    def importClubsAndPlayers(self):
        newClubs     = self._importClubs()
        newPlayers   = self._importPlayers()
        newRelations = self._importRelations()
        print("Fmported:\n"
            + "- %d new clubs\n"   % (newClubs)
            + "- %d new players\n" % (newPlayers)
            + "- %d new relations" % (newRelations)
            )

clubs = ImportClubsAndPlayers(
    config.cald.clubs['url'],
    config.cald.clubs['columns'],
    config.cald.clubs['delimiter'],
    )

clubs.importClubsAndPlayers()