#!/usr/bin/python
# coding=utf-8


clubs = dict(
    url       = 'http://archiv.cald.cz/caldMembersRecord/public/report/teams',
    # order is important
    columns   = ['ID oddílu', 'Oddíl', 'ID hráče', 'Příjmení', 'Jméno'],
    delimiter = '\t'
)

tournaments = dict(
    url       = 'http://archiv.cald.cz/caldMembersRecord/public/report/tournaments',
    # order is important
    columns   = ['ID turnaje', 'Název', 'Místo', 'Datum'],
    delimiter = '\t'
)

rosters = dict(
    url       = 'http://archiv.cald.cz/caldMembersRecord/public/report/rosters',
    # order is important
    columns   = ['ID turnaje', 'Název', 'ID Oddílu', 'Oddíl', 'Tým', 'ID hráče', 'Příjmení', 'Jméno'],
    delimiter = '\t'
)