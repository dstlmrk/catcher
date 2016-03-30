#!/usr/bin/python
# coding=utf-8

import urllib2
import sys, time
import config
import models as m

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

class Rosters(ImportFile):

    def __init__(self, *args):
        super(Rosters, self).__init__(*args)

    @m.db.atomic()
    def _importRosters(self):
        pass
        # TODO: only for development
        # with open('/home/marek/Dokumenty/bp/rosters') as f:
        #     self.body = f.read()
        # header, self.body = self._cutHeader(self.body)
        # only for development

    def importData(self):
        pass

class Tournaments(ImportFile):

    def __init__(self, *args):
        super(Tournaments, self).__init__(*args)

    def _getTournament(self, line):
        line = line.split(self.delimiter)
        # (id tournament, name, place, date)
        return (line[0], line[1], line[2], line[3])

    @m.db.atomic()
    def _importTournaments(self):
        # # TODO: only for development
        # with open('/home/marek/Dokumenty/bp/tournaments') as f:
        #     self.body = f.read()
        # header, self.body = self._cutHeader(self.body)
        # # only for development
        tournaments = set()
        for line in self.body:
            tournaments.add(self._getTournament(line))

        newTournaments = 0
        for tournament in tournaments:

            data = {
                'id'    : tournament[0],
                'name'  : tournament[1],
                'place' : tournament[2],
                'date'  : tournament[3]
            }

            try:
                m.CaldTournament.insert(**data).execute()
            except m.pw.IntegrityError as e:
                # duplicate rows will be not inserted
                pass
            else:
                newTournaments += 1
        return newTournaments

    def importData(self):
        newTournaments = self._importTournaments()
        print("Imported:\n"
            + "- %d new tournaments\n" % (newTournaments)
            )

class ClubsAndPlayers(ImportFile):

    def __init__(self, *args):
        super(ClubsAndPlayers, self).__init__(*args)

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

    @m.db.atomic()
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
                m.Club.insert(
                    caldId   = caldId,
                    name     = name,
                    shortcut = shortcut
                    ).execute()
            except m.pw.IntegrityError as e:
                # duplicate rows will be not inserted
                pass
            else:
                newClubs += 1
        return newClubs

    @m.db.atomic()
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
                m.Player.insert(
                    caldId    = caldId,
                    lastname  = lastname,
                    firstname = firstname
                    ).execute()
            except m.pw.IntegrityError as ex:
                # duplicate rows will be not inserted
                pass
            else:
                newPlayers += 1


        return newPlayers

    @m.db.atomic()
    def _importRelations(self):
        relations = set()
        for line in self.body:
            relations.add(self._getRelation(line))

        newRelations = 0

        for relation in relations:
            clubCaldId   = int(relation[0])
            playerCaldId = int(relation[1])

            try:
                club = m.Club.get(caldId=clubCaldId)
                player = m.Player.get(caldId=playerCaldId)
            except m.Club.DoesNotExist as ex:
                print("Club %d (cald id) doesn't exist" % (clubCaldId))
                continue
            except m.Player.DoesNotExist as ex:
                print("Player %d (cald id) doesn't exist" % (playerCaldId))
                continue

            try:
                # create new relation
                m.ClubHasPlayer.insert(
                    club         = club,
                    player       = player,
                    caldRelation = False
                    ).execute()
            except m.pw.IntegrityError as ex:
                # if exists, ignore it
                pass

            clubHasPlayer = m.ClubHasPlayer.get(club=club, player=player)
            if not clubHasPlayer.caldRelation:
                # somewhere exists old relation
                    m.ClubHasPlayer.update(
                        caldRelation = False
                    ).where(
                        m.ClubHasPlayer.caldRelation == True,
                        m.ClubHasPlayer.player == player
                    ).execute()
                    # set new relation
                    qr = m.ClubHasPlayer.update(
                        caldRelation = True
                    ).where(
                        m.ClubHasPlayer.club == club,
                        m.ClubHasPlayer.player == player
                    ).execute()
                    newRelations += int(qr)

        return newRelations

    def importData(self):
        newClubs     = self._importClubs()
        newPlayers   = self._importPlayers()
        newRelations = self._importRelations()
        print("Imported:\n"
            + "- %d new clubs\n"   % (newClubs)
            + "- %d new players\n" % (newPlayers)
            + "- %d new relations" % (newRelations)
            )


if __name__ == "__main__":

    start_time = time.time()
    m.db.connect()

    clubs = ClubsAndPlayers(
        config.cald.clubs['url'],
        config.cald.clubs['columns'],
        config.cald.clubs['delimiter']
        ).importData()

    tournaments = Tournaments(
        config.cald.tournaments['url'],
        config.cald.tournaments['columns'],
        config.cald.tournaments['delimiter']
        ).importData()

    rosters = Rosters(
        config.cald.rosters['url'],
        config.cald.rosters['columns'],
        config.cald.rosters['delimiter']
        ).importData()

    if not m.db.is_closed():
        m.db.close()

    print("= %s seconds" % (time.time() - start_time))
