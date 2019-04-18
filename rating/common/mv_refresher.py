import threading

from django.conf import settings

from django.db import connection
from time import sleep


class MVRefresherThread(threading.Thread):

    def run(self):
        while True:
            with connection.cursor() as cursor:
                cursor.execute('select refresh_leaderboard_mv();') # we're calling psql function instead of direct refreshing to prevent spawning idle queries in pg_stat_activity;
            sleep(60)
