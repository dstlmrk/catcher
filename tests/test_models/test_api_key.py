from catcher.models import User, ApiKey
from datetime import datetime, timedelta
import time


def test_api_key_prolong_validity(session, users):
    user, api_key, valid_to = User.log_in(session, "user1", "password1")
    token = session.query(ApiKey).get(api_key)
    assert valid_to == token.valid_to.strftime('%Y-%m-%d %H:%M:%S')
    # it's necessary because prolong validity
    time.sleep(1)
    ApiKey.prolong_validity(session, api_key)
    prolonged_token = session.query(ApiKey).get(api_key)
    valid_to_obj = datetime.strptime(valid_to, '%Y-%m-%d %H:%M:%S')
    prolonged_valid_to_obj = datetime.strptime(
        prolonged_token.valid_to, '%Y-%m-%d %H:%M:%S'
    )
    assert valid_to_obj + timedelta(seconds=1) == prolonged_valid_to_obj


def test_api_key_create(session, users):
    user = User.get(session, 1)
    api_key, valid_to = ApiKey.create(session, user)
    assert isinstance(api_key, str)
    assert datetime.strptime(valid_to, '%Y-%m-%d %H:%M:%S')
