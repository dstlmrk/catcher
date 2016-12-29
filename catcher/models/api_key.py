#

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from catcher.models.base import Base
from catcher.config import config

import datetime
import uuid


class ApiKey(Base):
    __tablename__ = 'api_key'

    key = Column(String, primary_key=True)
    valid_to = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return "<ApiKey(key='%s', valid_to='%s', user_id='%s')>" % (
            self.key, self.valid_to, self.user_id)

    @staticmethod
    def create(user, session):
        """
        :param user: User object.
        :param session: Session should be created only once so here is as parameter.
        :return: Key and its validity.
        """
        key = ApiKey._generate_key(session)
        valid_to = ApiKey._get_validity()
        session.add(ApiKey(key=key, valid_to=valid_to, user_id=user.id))
        return key, valid_to

    @staticmethod
    def cancel_validity(api_key, session):
        """
        """

    @staticmethod
    def _get_validity():
        validity = int(config['api']['key_validity'])
        valid_to = datetime.datetime.now() + datetime.timedelta(minutes=validity)
        return valid_to.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def _generate_key(session):
        """
        :return: Random api key.
        """
        for i in range(10):
            key = uuid.uuid4().hex
            if not session.query(ApiKey).get(key):
                return key
            else:
                continue
        raise RuntimeError("It couldn't generate new api key, please try it again")
