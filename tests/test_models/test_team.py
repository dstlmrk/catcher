from catcher.models import Team


def test_team_get(session, teams):
    assert Team.get(session, id=1) == session.query(Team).get(1)


def test_team_get_all(session, teams):
    teams_count = session.query(Team).count()
    assert len(Team.get_all(session)) == teams_count


def test_team_create(session):
    teams_count = session.query(Team).count()
    team = Team.create(session, name="FC Brno", shortcut="FCB",
                       division_id=1,
                       city="Brno", country="CZE")
    assert team.name == "FC Brno"
    assert (teams_count + 1) == session.query(Team).count()
    team = session.query(Team).filter_by(name="FC Brno").one()
    assert team.shortcut == "FCB"
    assert team.division_id == 1
    assert team.division.type == "open"


def test_team_delete(session, teams):
    assert session.query(Team).get(1).deleted == False
    Team.delete(session, id=1)
    assert session.query(Team).get(1).deleted == True


def test_team_edit(session):
    team = Team.create(session, name="FC Brno", shortcut="FCB", division_id=1,
                       city="Brno", country="CZE")
    session.commit()
    Team.edit(session, id=team.id, shortcut="XXX", city="Olomouc")
    edited_team = session.query(Team).get(team.id)
    assert edited_team.shortcut == "XXX"
    assert edited_team.city == "Olomouc"
