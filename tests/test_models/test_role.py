from catcher.models import Role


def test_role_get_all(session):
    roles_count = session.query(Role).count()
    roles = Role.get_all(session)
    assert len(roles) == roles_count
    assert isinstance(roles, list)
