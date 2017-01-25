from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, joinedload
from catcher.models.base import Base, CountryCode


SHORTCUT_MAX_LENGTH = 3


class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    shortcut = Column(String)
    division_id = Column(Integer, ForeignKey('division.id'))
    division = relationship("Division")
    deleted = Column(Boolean, default=False)
    city = Column(String)
    country = Column(CountryCode)
    cald_id = Column(Integer)
    user_id = Column(Integer)

    @staticmethod
    def get(session, id):
        """Get team by id"""
        return session.query(Team).get(id)

    @staticmethod
    def create(session, name, shortcut, division_id, city,
               country, cald_id=None, user_id=None):
        """Create new team"""
        team = Team(name=name, shortcut=shortcut[:SHORTCUT_MAX_LENGTH],
                    division_id=division_id, city=city, country=country,
                    cald_id=cald_id, user_id=user_id)
        session.add(team)
        return team

    @staticmethod
    def get_all(session, **kwargs):
        """Get all teams"""
        return [
            team for team in session.query(Team)\
                                    .options(joinedload('division'))\
                                    .filter_by(**kwargs)
        ]

    @staticmethod
    def delete(session, id):
        """Set delete flag for team"""
        team = session.query(Team).get(id)
        if team.deleted:
            return False
        team.deleted = True
        return True

    @staticmethod
    def edit(session, id, name=None, shortcut=None, division_id=None,
             city=None, country=None, cald_id=None):
        """Edit team's attributes"""
        team = session.query(Team).get(id)
        if name:
            team.name = name
        if shortcut:
            team.shortcut = shortcut[:SHORTCUT_MAX_LENGTH]
        if division_id:
            team.division_id = division_id
        if city:
            team.city = city
        if country:
            team.country = country
        if cald_id:
            team.cald_id = cald_id
        return team
