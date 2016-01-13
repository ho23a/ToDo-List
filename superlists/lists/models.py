# from __future__ import unicode_literals
from django.db import models

class List(models.Model):
    pass

# models.Model extension gives Item the methods (e.g. save() )
class Item(models.Model):
    # '' when an item first created
    text = models.TextField(default='')
    # list is a property
    list = models.ForeignKey(List, default=None)
    is_done = models.BooleanField(default=False)
