User
====

.. http:get:: /api/user/(int:id)
  
  Get user by id.

  **Example request**:

  .. sourcecode:: http

    GET /api/user/1 HTTP/1.1
    Host: catcher.zlutazimnice.cz
    
  **Example response**:

  .. sourcecode:: http

    HTTP/1.1 200 OK
    Content-Type: application/json; charset=UTF-8

    {
      "created_at": "2017-01-29T14:29:53",
      "login": "bad_user_92",
      "email": "mycoolemail@gmail.com",
      "role_id": 1,
      "id": 1
    }

  :>jsonarr int id: id
  :>jsonarr timestamp created_at: time of creation
  :>jsonarr string login: user's login
  :>jsonarr string email: user's email
  :>jsonarr int role_id: role id (admin, user, etc.)

  :statuscode 200: no error
  :statuscode 401: not found
  :statuscode 404: not found

.. http:put:: /api/user/(int:id)
  
  Edit the user. User can edit only himself (or admin). 

  :jsonparam string login: user's login (available for admin only)
  :jsonparam string email: user's email
  :jsonparam string password: new password
  :jsonparam string old_password: old password (required if password is filled)
  :jsonparam int role_id: role id (available for admin only)

  :statuscode 200: no error
  :statuscode 401: unauthorized
  :statuscode 404: not found

.. http:delete:: /api/user/(int:id)
  
  Delete user. It's available only for admin. 

  :statuscode 200: no error
  :statuscode 401: unauthorized
  :statuscode 404: not found

.. http:get:: /api/users

  All users without any specific parametrize the query.

  **Example request**:

  .. sourcecode:: http

    GET /api/users HTTP/1.1
    Host: catcher.zlutazimnice.cz
    
  **Example response**:

  .. sourcecode:: http

    HTTP/1.1 200 OK
    Content-Type: application/json; charset=UTF-8

    {
      "users": []
    }

  :statuscode 200: no error

.. http:post:: /api/users

  Create new user. It's available only for admin. 

  :jsonparam string login: user's login
  :jsonparam string email: user's email
  :jsonparam string password: user's password
  :jsonparam int role_id: role id (admin, user, etc.)

  :statuscode 201: user is created
  :statuscode 401: unauthorized
