#!/usr/bin/python
# coding=utf-8

from catcher.models import Team, Division


def test_team_get(session, teams):
    assert Team.get(id=1) == session.query(Team).get(1)


def test_team_create(session):
    team_count = session.query(Team).count()
    team_division_id = session.query(Division) \
                              .filter(Division.type=="open") \
                              .one().id
    session.commit()
    team = Team.create(name="FC Brno", shortcut="FCB",
                       division_id=team_division_id,
                       city="Brno", country="CZE")

    assert team.name == "FC Brno"
    assert team_count + 1 == session.query(Team).count()

    team = session.query(Team).filter_by(name="FC Brno").one()

    assert team.shortcut == "FCB"
    assert team.division_id == team_division_id
    assert team.division.type == "open"


def test_team_delete(session, teams):
    assert session.query(Team).get(1).deleted == False
    Team.delete(id=1)
    # drops data from cache also
    session.commit()
    assert session.query(Team).get(1).deleted == True


def test_team_edit(session):
    team = Team.create(name="FC Brno", shortcut="FCB", division_id=1,
                       city="Brno", country="CZE")
    Team.edit(id=team.id, shortcut="XXX", city="Olomouc")
    edited_team = session.query(Team).get(team.id)
    assert edited_team.shortcut == "XXX"
    assert edited_team.city == "Olomouc"
