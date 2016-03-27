# Catcher API 2.0

Více na catcher.zlutazimnice.cz

## Dependencies
```
python2.7
python-minimal
python-pip
python-dev
build-essential
libpcre3
libpcre3-dev
nginx
libmysqlclient-dev
percona-server-server-5.5

uwsgi
peewee
falcon
iso3166
MySQL-python
```

## Local deploy
```
$ uwsgi --http :9090 --wsgi-file restapi.py --callable app
```

## Server deploy
```
uwsgi --socket localhost:8080 --wsgi-file ./restapi.py --callable api &
```

## Sym links
```
ln -s /home/dstlmrk/catcher/nginx/catcher.conf /etc/nginx/sites-enabled/
ln -s /home/dstlmrk/catcher/html/ /var/www/catcher
ln -s /home/dstlmrk/catcher/ /usr/local/lib/python2.7/dist-packages/catcher
```