# #!/usr/bin/python
# # coding=utf-8

# -------------------------------------------------------------------------------------------------
# TODO: tady zacnu simulovat pozadavky rest api, naimportuju modely a budu volat jejich metody,
# TODO: aniz bych pouzil falcon nejakou dobu tedy nebudu potrebovat resources (falcon) ani uwsgi
# -------------------------------------------------------------------------------------------------
# TODO: psat testy na modely?
# -------------------------------------------------------------------------------------------------


# TODO: uzivateli pridam sloupec valid_to, ktery bude slouzit pro odhlasovani a platnosti api tokenu
# TODO: jmeno sloupce? validity? valid_to? api_key_valid_to?

# TODO: podivat se, jak by to slo udelat jinak


from catcher import models


# -----------------------------------------------------
# Create first api_keys
# -----------------------------------------------------
key, valid_to = models.User.login(email='vesel@test.cz', password='heslo')
print(key, valid_to)
models.User.logout(api_key=key)


# def to_floats(func):
#     def outer_function(a, b):
#         a = float(a)
#         b = float(b)
#         print("XXX1")
#         retval = func(a, b)
#         print("XXX2")
#         return retval
#
#     return outer_function
#
#
# @to_floats
# def add(a, b):
#     """Adds two numbers"""
#     return a + b
#
#
#
# print(add(1, '2'))

