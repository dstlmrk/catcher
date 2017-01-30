Catcher's documentation
=======================

Tato dokumentace slouží k popisu serverové části webové aplikace Catcher. V jedné části je popis pro REST API, které je dostupné klientům, a ve druhé popis samotného kódu.

What is the Catcher?
--------------------
Catcher je aplikace sloužící pro správu turnajů v Ultimate Frisbee. Zjednodušuje práci organizátorům a ostatním poskytuje podrobné statistiky zápasů a hodnocení SOTG.

REST API
--------

Authorization and authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Uživatel se přihlašuje svým emailem a heslem. Po přihlášení je mu sdělen přístupový token, kterým lze přistupovat až do vypršení jeho platnosti. Doba jeho platnosti je s každým použitím prodloužena. Jeden uživatel může být přihlášen na více zařízeních pomocí více tokenů.

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

These headers aren't in examples because are sended in every time from server with the same value except ``content-length``.

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

Catcher je balen jako Python balíček. Nejde ale o open source, proto jej nenajdete nikde ke stáhnutí.

- Aplikace potřebuje pro svůj běh konfigurační soubor. V souboru `conf/catcher.test.cfg` je nastavení pro testovací prostředí.
- Vyžaduje připojení do databáze MySQL (nastaveno v konfiguračním souboru).
- Pro automatické testování se používá Travis CI.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
