Team
====

.. http:get:: /api/team/(int:id)
  
  Get team by id.

  **Example request**:

  .. sourcecode:: http

    GET /api/team/1 HTTP/1.1
    Host: catcher.zlutazimnice.cz
    
  **Example response**:

  .. sourcecode:: http

    HTTP/1.1 200 OK
    Content-Type: application/json; charset=UTF-8

    {
      "city": "Praha",
      "division_id": 1,
      "deleted": false,
      "shortcut": "PD",
      "country": "CZE",
      "user_id": null,
      "cald_id": null,
      "id": 1,
      "name": "Prague Devils"
    }

  :>jsonarr int id: id
  :>jsonarr string name: name
  :>jsonarr string shortcut: three-letter shortcut which is'n unique
  :>jsonarr bool deleted: true if team is deleted
  :>jsonarr string city: team's city
  :>jsonarr string country: team's country by ISO 3166-1 alpha-3
  :>jsonarr int division_id: id of the division (open, women, etc.)
  :>jsonarr int user_id: owner id
  :>jsonarr int cald_id: cald tournament id

  :statuscode 200: no error
  :statuscode 404: not found

.. http:put:: /api/team/(int:id)
  
  Edit the team. It's available only for admin and owner. 

  :jsonparam string name: name
  :jsonparam string shortcut: three-letter shortcut which is'n unique
  :jsonparam string city: team's city
  :jsonparam string country: team's country by ISO 3166-1 alpha-3
  :jsonparam int division_id: id of the division (open, women, etc.)
  :jsonparam int cald_id: cald tournament id

  :statuscode 200: no error
  :statuscode 401: unauthorized
  :statuscode 404: not found

.. http:delete:: /api/team/(int:id)

  Set flag signalling if the team is deleted to true. It's available only for admin. 

  :statuscode 200: no error
  :statuscode 401: unauthorized
  :statuscode 404: not found

.. http:get:: /api/teams

  All teams without any specific parametrize the query.

  **Example request**:

  .. sourcecode:: http

    GET /api/teams HTTP/1.1
    Host: catcher.zlutazimnice.cz
    
  **Example response**:

  .. sourcecode:: http

    HTTP/1.1 200 OK
    Content-Type: application/json; charset=UTF-8

    {
      "teams": []
    }

  :statuscode 200: no error

.. http:post:: /api/teams

  Create new team.

  :jsonparam string name: name
  :jsonparam string shortcut: three-letter shortcut which is'n unique
  :jsonparam string city: team's city
  :jsonparam string country: team's country by ISO 3166-1 alpha-3
  :jsonparam int division_id: id of the division (open, women, etc.)
  :jsonparam int cald_id: cald tournament id
  :jsonparam int user_id: owner id

  :statuscode 201: team is created