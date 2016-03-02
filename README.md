## Dependencies
```
peewee
falcon
```

## Local deploy
```
$ uwsgi --http :9090 --wsgi-file restapi.py --callable app
```