#

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
# from sqlalchemy.orm.exc import NoResultFound
from catcher.models.base import Base, session, CountryCode
from catcher.models import Division

SHORTCUT_MAX_LENGTH = 3


class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    shortcut = Column(String)
    division_id = Column(Integer, ForeignKey('division.id'))
    city = Column(String)
    country = Column(CountryCode)
    cald_id = Column(Integer)
    user_id = Column(Integer)

    @staticmethod
    @session
    def get(id, _session):
        return _session.query(Team).get(id)

    @staticmethod
    @session
    def create(name, shortcut, division, city, country,
               _session, cald_id=None, user_id=None):
        division_id = _session.query(Division).filter(Division.type == division).one().id
        team = Team(name=name, shortcut=shortcut[:SHORTCUT_MAX_LENGTH],
                    division_id=division_id, city=city, country=country,
                    cald_id=cald_id, user_id=user_id)
        _session.add(team)
        return team

    @staticmethod
    @session
    def delete(id, _session):
        _session.query(Team).filter(Team.id == id).delete()

    @staticmethod
    @session
    def edit(id, _session, name=None, shortcut=None, division=None,
             city=None, country=None, cald_id=None):
        team = _session.query(Team).get(id)
        if name:
            team.name = name
        if shortcut:
            team.shortcut = shortcut[:SHORTCUT_MAX_LENGTH]
        if division:
            division_id = _session.query(Division).filter(
                Division.type == division
            ).one().id
            team.division_id = division_id
        if city:
            team.city = city
        if country:
            team.country = country
        if cald_id:
            team.cald_id = cald_id
