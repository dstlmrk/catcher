Login and Registration
======================

.. http:post:: /api/registration
   
   Po vytvoření uživatele přijde na uvedený email automaticky vygenerované heslo. Je doporučeno jej změnit co nejdříve po registraci.

   **Example request**:

   .. sourcecode:: http

      POST /api/registration HTTP/1.1
      Host: catcher.zlutazimnice.cz
      Content-Type: application/json
      
      {
        "login": "bad_user_92",
        "email": "mycoolemail@gmail.com"
      }

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 201 Created

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 400 Bad Request
      content-type: application/json; charset=UTF-8

      {
         "title": "ValueError",
         "description": "User already exists with this login or email"
      }

   :jsonparam string login: an unique login for user logging
   :jsonparam string email: generate password will send there

   :statuscode 201: user is created and password is sended
   :statuscode 400: bad request

.. http:post:: /api/login

   Vytvoří token platný pro následujících 15 minut. Každé jeho použití jeho platnost posunuje tak, aby následujících 15 minut zůstal platný.

   **Example request**:

   .. sourcecode:: http

      POST /api/registration HTTP/1.1
      Host: catcher.zlutazimnice.cz
      Content-Type: application/json
      
      {
        "login": "bad_user_92",
        "password": "FrE812x"
      }

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 201 Created
      content-type: application/json; charset=UTF-8

      {
         "valid_to": "2017-01-29 14:45:37",
         "user": {
          "id": 1,
          "created_at": "2017-01-29T14:29:53",
          "role": {
            "type": "user",
            "id": 1
          },
          "login": "bad_user_92",
          "role_id": 2,
          "email": "mycoolemail@gmail.com"
         },
         "api_key": "ca5d697312b547cd977207c4128ff152"
      }

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 401 Unauthorized
      content-type: application/json; charset=UTF-8

      {
         "title": "Authentication Failed",
         "description": "Login or password is wrong."
      }

   :jsonparam string login: user's login
   :jsonparam string password: user's password

   :>jsonarr datetime valid_to: datetime when token will expire
   :>jsonarr json user: user object 
   :>jsonarr api_key string: token for another use

   :statuscode 201: user logged
   :statuscode 401: unauthorized
