Division
========

.. http:get:: /api/divsions
	
	All divisions without any specific parametrize the query.

  **Example request**:

  .. sourcecode:: http

    GET /api/divisions HTTP/1.1
    Host: catcher.zlutazimnice.cz
    
  **Example response**:

  .. sourcecode:: http

    HTTP/1.1 200 OK
    Content-Type: application/json; charset=UTF-8

    {
      "divisions": [
        {
          "id": 3,
          "type": "mixed"
        },
        {
          "id": 1,
          "type": "open"
        },
        {
          "id": 2,
          "type": "women"
        }
      ]
    }

  :statuscode 200: no error
