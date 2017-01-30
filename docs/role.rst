Role
====

.. http:get:: /api/roles
	
	All roles without any specific parametrize the query.

  **Example request**:

  .. sourcecode:: http

    GET /api/roles HTTP/1.1
    Host: catcher.zlutazimnice.cz
    
  **Example response**:

  .. sourcecode:: http

    HTTP/1.1 200 OK
    Content-Type: application/json; charset=UTF-8

    {
      "roles": [
        {
          "id": 2,
          "type": "admin"
        },
        {
          "id": 1,
          "type": "user"
        }
      ]
    }

  :statuscode 200: no error
