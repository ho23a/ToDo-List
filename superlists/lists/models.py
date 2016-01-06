# from __future__ import unicode_literals
from django.db import models

# models.Model extension gives Item the methods
class Item(models.Model):
    # '' when an item first created
    text = models.TextField(default='')
