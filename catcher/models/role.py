#

from sqlalchemy import Column, Integer, String
from catcher.models.base import Base


class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    type = Column(String)
