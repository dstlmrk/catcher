## Dependencies
```
peewee
falcon
iso3166
```

## Local deploy
```
$ uwsgi --http :9090 --wsgi-file restapi.py --callable app
```
