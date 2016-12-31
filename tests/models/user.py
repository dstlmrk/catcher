#!/usr/bin/python
# coding=utf-8

from catcher.models import User, Role, ApiKey
from sqlalchemy.orm.exc import NoResultFound
import pytest


def test_user_get(session, users):
    assert User.get(id=1) == session.query(User).get(1)


def test_user_create(session):
    user_count = session.query(User).count()
    user_email = "karel@email.cz"
    user_login = "karel"
    user_role = "organizer"
    user_role_id = session.query(Role).filter(Role.type == user_role).one().id

    # pred zavolanim models, musim zavolat commit, protoze uvnitr zacina nova transakce
    session.commit()

    user = User.create(login="karel", email="karel@email.cz", role="organizer")

    assert user.email == "karel@email.cz"
    assert user_count+1 == session.query(User).count()

    user = session.query(User).filter_by(email=user_email).one()

    assert user.login == "karel"
    assert user.role_id == user_role_id


def test_user_edit(session):
    user = User.create(login="karel", email="karel@email.cz", role="organizer")
    User.edit(id=user.id, email="novak@test.com", password="test_password")
    edited_user = session.query(User).get(user.id)
    assert edited_user.email == "novak@test.com"
    assert edited_user.password == "test_password"


def test_user_login(session, users):
    user = session.query(User).first()
    session.commit()
    User.edit(id=user.id, password="test_password")
    key, valid_to = User.log_in(login=user.login, password="test_password")
    # check api_key
    api_key = session.query(ApiKey).filter_by(user_id=user.id).one()
    assert api_key.key == key
    assert str(api_key.valid_to) == str(valid_to)


def test_user_logout(session, users):
    user = session.query(User).first()
    session.commit()
    User.edit(id=user.id, password="test_password")
    # login
    key, valid_to = User.log_in(login=user.login, password="test_password")
    # logout
    User.log_out(api_key=key)
    # check api_key
    with pytest.raises(NoResultFound):
        session.query(ApiKey).filter_by(user_id=user.id).one()
