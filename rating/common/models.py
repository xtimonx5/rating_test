from django.db import models
from django.db.models import Index
from django.utils.timezone import now


class RateRecord(models.Model):
    user_id = models.IntegerField(primary_key=True, db_index=True)
    rating = models.FloatField(null=False, db_index=True)
    datetime = models.DateTimeField(default=now)

    class Meta:
        indexes = [
            Index(fields=['-rating', 'datetime']),  # default index is desc
        ]


class LeaderBoard(models.Model):  # to allow use materialized view as common django model in read-only mode
    rate_place = models.IntegerField(db_column='rate_place', primary_key=True)
    user_id = models.IntegerField('user_id')
    rating = models.FloatField(db_column='rating', )
    datetime = models.DateTimeField(db_column='datetime')

    class Meta:
        db_table = 'leaderboard'
        managed = False
