# #!/usr/bin/python
# # coding=utf-8

from catcher import models

# -----------------------------------------------------
# Create first users
# -----------------------------------------------------
models.User.create(email='vesel@test.cz', role='admin')
models.User.create(email='dosta@test.cz', role='admin')
models.User.create(email='organizer@test.cz', role='organizer')

# -----------------------------------------------------
# Create api_key for test only
# -----------------------------------------------------
key, valid_to = models.User.login(email='vesel@test.cz', password='heslo')
models.User.logout(api_key=key)

# -----------------------------------------------------
# Create first teams
# -----------------------------------------------------

