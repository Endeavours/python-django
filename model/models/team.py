__author__ = 'prasanna'

from django.db import models

class Team(models.Model):
    """
    Represents a team
    """
    name = models.CharField(max_length=16)
    created_on = models.DateTimeField(auto_now_add=True)