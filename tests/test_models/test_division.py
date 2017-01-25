from catcher.models import Division


def test_division_get_all(session):
    divisions_count = session.query(Division).count()
    divisions = Division.get_all(session)
    assert len(divisions) == divisions_count
    assert isinstance(divisions, list)
