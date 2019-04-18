from django.core.cache import cache
from django.db import connection
from django.test import TestCase


class CommonRatingTest(TestCase):
    def setUp(self):
        self._refresh_mat_view()
        cache.clear()

    def _refresh_mat_view(self):
        with connection.cursor() as cursor:
            cursor.execute('REFRESH MATERIALIZED VIEW leaderboard;')
