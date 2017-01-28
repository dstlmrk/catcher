# #!/usr/bin/python
# # coding=utf-8

from catcher import models
from catcher.models.base import Session

session = Session()

# TODO: tady se vklada vse, co bude potreba pro zakladni beh aplikace (slouzi predevsim pro testovani)
# -----------------------------------------------------
# Create first users
# -----------------------------------------------------
models.User.create(session, login='vesel', email='vesel@test.cz', password="hesloo", role_id=2)
models.User.create(session, login='dost', email='dosta@test.cz', password="hesloo", role_id=2)
models.User.create(session, login='org', email='organizer@test.cz', password="hesloo", role_id=1)

# -----------------------------------------------------
# Create first teams
# -----------------------------------------------------
models.Team.create(session, name="Prague Devils", shortcut="PD", city="Praha", country="CZE", division_id=1)
models.Team.create(session, name="Žlutá Zimnice", shortcut="ŽZ", city="Praha", country="CZE", division_id=2)
