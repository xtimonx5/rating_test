import threading
from time import sleep

from django.core.cache import cache
from django.db import connection


class MVRefresherThread(threading.Thread):
    def run(self):
        while True:
            with connection.cursor() as cursor:
                cursor.execute(
                    'select refresh_leaderboard_mv();')  # we're calling psql function instead of direct refreshing to prevent spawning idle queries in pg_stat_activity;

            cache.clear()
            sleep(60)
