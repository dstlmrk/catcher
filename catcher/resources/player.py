#!/usr/bin/python
# coding=utf-8

from api.resource import Collection, Item
import models as m
import falcon
import peewee as pw

class Player(Item):
    pass

class Players(Collection):
    pass