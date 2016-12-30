# #!/usr/bin/python
# # coding=utf-8

from catcher import models

# -----------------------------------------------------
# Create first users
# -----------------------------------------------------
models.User.create(login='vesel', email='vesel@test.cz', role='admin')
models.User.create(login='dost', email='dosta@test.cz', role='admin')
models.User.create(login='org', email='organizer@test.cz', role='organizer')

# -----------------------------------------------------
# Create api_key for test only
# -----------------------------------------------------
key, valid_to = models.User.log_in(login='vesel', password='heslo')
models.User.logout(api_key=key)

# -----------------------------------------------------
# Create first teams
# -----------------------------------------------------

