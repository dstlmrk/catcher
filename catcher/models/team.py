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
    def create(name, shortcut, division, city, country,
               _session, cald_id=None, user_id=None):
        division_id = _session.query(Division).filter(Division.type == division).one().id
        team = Team(name=name, shortcut=shortcut[:SHORTCUT_MAX_LENGTH],
                    division_id=division_id, city=city, country=country,
                    cald_id=cald_id, user_id=user_id)
        _session.add(team)

    @staticmethod
    @session
    def delete(id, _session):
        pass

    @staticmethod
    @session
    def edit(id, name, shortcut, division, city, country, cald_id, user_id):
        # TODO: muze uzivatel zmenit majitele?
        # TODO: tady jsem skoncil, oc vsechno muze menit atd.?
        pass

    # email = Column(String)
    # password = Column(String)
    # created_at = Column(DateTime, default=time.strftime('%Y-%m-%d %H:%M:%S'))
    # role_id = Column(Integer, ForeignKey('role.id'))
    #


# id, division_id, name, shortcut, city, country, cald_id, user_id