from django.db import models
from django.contrib.auth.models import User

class Tokens(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
        db_column='user', blank=True, null=True)
    token = models.CharField(primary_key=True, max_length=45, unique=True)
    tg_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tokens'

class Messages(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True,
        db_column='user', related_name='messages')
    message = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'messages'