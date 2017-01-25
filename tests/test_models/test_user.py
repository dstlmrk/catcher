from catcher.models import User, NullUser
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
import pytest


def test_user_get(session, users):
    assert User.get(session, 1) == session.query(User).get(1)


def test_user_get_by_auth(session, users):
    logged_user, api_key, valid_to = User.log_in(session, "user1", "password1")
    user = User.get_by_auth(session, api_key)
    assert logged_user == user


def test_user_log_in(session, users):
    user, api_key, valid_to = User.log_in(session, "user1", "password1")
    assert user.id == 1


def test_user_log_in_invalid(session, users):
    with pytest.raises(NoResultFound):
        User.log_in(session, "user1", "badpassword")


def test_user_get_all(session, users):
    users_count = session.query(User).count()
    assert len(User.get_all(session)) == users_count


def test_user_create(session):
    created_user = User.create(session, "login", "test@test.cz", "password", 1)
    session.commit()
    user = session.query(User).get(created_user.id)
    assert created_user == user


def test_user_create_invalid(session, users):
    with pytest.raises(IntegrityError):
        User.create(session, "user1", "user1@test.cz", "password1", 1)
        session.commit()


@pytest.mark.skip()
def test_user_register(session):
    pass


@pytest.mark.skip()
def test_user_register_invalid(session):
    pass


def test_user_delete(session, users):
    users_count = session.query(User).count()
    User.delete(session, 1)
    assert users_count == session.query(User).count() + 1


def test_user_edit(session):
    user = User.create(session, "login", "test@test.cz", "password", 1)
    session.commit()
    User.edit(session, user.id, email="new@email.cz", role_id=2)
    edited_user = session.query(User).get(user.id)
    assert edited_user.email == "new@email.cz"
    assert edited_user.role_id == 2


def test_user_edit_invalid(session):
    with pytest.raises(ValueError):
        User.edit(session, 1, email="bad_email_format", role_id=2)


def test_null_user():
    null_user = NullUser()
    for key, value in null_user.__dict__.items():
        assert value is None
