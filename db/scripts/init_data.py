# #!/usr/bin/python
# # coding=utf-8

from catcher import models

# TODO: tady se vklada vse, co bude potreba pro zakladni beh aplikace (slouzi predevsim pro testovani)
# -----------------------------------------------------
# Create first users
# -----------------------------------------------------
models.User.create(login='vesel', email='vesel@test.cz', role='admin')
models.User.create(login='dost', email='dosta@test.cz', role='admin')
models.User.create(login='org', email='organizer@test.cz', role='user')

# -----------------------------------------------------
# Create api_key for test only
# -----------------------------------------------------
key, valid_to = models.User.log_in(login='vesel', password='heslo')
models.User.log_out(api_key=key)

# -----------------------------------------------------
# Create first teams
# -----------------------------------------------------
models.Team.create(name="Prague Devils", shortcut="PD", city="Praha", country="CZE", division="open")
models.Team.create(name="Prague Devils", shortcut="PD", city="Praha", country="CZE", division="women")
