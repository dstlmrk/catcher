Catcher's documentation
=======================

This documentation is intended to describe the server-side of a web application Catcher. The first part is dedicated to the REST API description, the second deals with description of the code itself.

What is the Catcher?
--------------------
The Catcher is an application designed for the administration of Ultimate Frisbee tournaments. It simplifies the work of the organizers and provides detailed match and SOTG score statistics.

REST API
--------

Authorization and authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The user logs in with his email and password. After a successful login, he is given an access token that can be used until it expires. The token validity is refreshed with every request with auth header. A single user can be logged into his account on multiple devices using several tokens.

Headers
~~~~~~~

Keep in mind that Catcher API only supports responses encoded as JSON.

Client
^^^^^^

Only these headers are necessary.

- ``Content-Type`` - for POST and PUT requests
- ``Authorization`` - for requests where authentication is required

Server
^^^^^^

These headers are not in examples because they are sent in every time from the server with the same value except ``content-length``.

- ``access-control-allow-headers: Content-Type,Authorization,X-Name``
- ``access-control-allow-methods: PUT,POST,DELETE,GET``
- ``access-control-allow-origin: *``
- ``content-length: 145``
- ``content-type: application/json; charset=UTF-8``

Resources
~~~~~~~~~

.. toctree::
   :maxdepth: 1

   login
   user
   team
   division
   role

Python package
--------------

The Catcher is prepared as a Python package. As it is not an open source though, it is not available for download.

- The application requires a configuration file for its operation. The settings for test environment can be found in the ``conf/catcher.test.cfg`` file.
- MySQL database connection is required (set in the configuration file).
- `Travis CI`__ is used for the automatical testing.

.. _Travis: https://travis-ci.org/dstlmrk/catcher
__ Travis_

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
