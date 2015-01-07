__author__ = 'prasanna'

from django.db import models
from django.conf import settings

class Manager(models.Model):
    """
    represents the manager data
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    teams = models.ForeignKey()