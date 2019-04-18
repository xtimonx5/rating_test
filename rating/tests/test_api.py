import json
from datetime import datetime
from random import random

from rest_framework.test import APIClient

from common.models import RateRecord
from .common import CommonRatingTest


class LeaderBoardApiTestCase(CommonRatingTest):
    def setUp(self):
        super(LeaderBoardApiTestCase, self).setUp()
        self.client = APIClient()
        for x in range(100, 200):
            RateRecord.objects.create(user_id=x, rating=random(), datetime=datetime.now())
        self._refresh_mat_view()

    def test_list(self):
        response = self.client.get('/api/leaderboard/?limit=100')
        response_dict = json.loads(response.content)
        results = response_dict['results']
        self.assertEqual(response_dict['count'], 100)
        self.assertEqual(len(results), 100)
        self.assertEqual(results[0]['user_id'], RateRecord.objects.earliest('-rating', 'datetime').user_id)
        self.assertEqual(results[-1]['user_id'], RateRecord.objects.latest('-rating', 'datetime').user_id)

    def test_pagination(self):
        # default pagination is 20 elements
        response = self.client.get('/api/leaderboard/')
        response_dict = json.loads(response.content)
        self.assertEqual(response_dict['count'], 100)
        self.assertEqual(len(response_dict['results']), 20)

        response = self.client.get('/api/leaderboard/?limit=5')
        response_dict = json.loads(response.content)
        self.assertEqual(response_dict['count'], 100)
        self.assertEqual(len(response_dict['results']), 5)

    def test_query_params(self):
        # testing exact rate place
        response_exact_rate_place = self.client.get('/api/leaderboard/?rate_place=5')
        response_dict = json.loads(response_exact_rate_place.content)
        self.assertEqual(response_dict['results'][0]['rate_place'], 5)

        # testing `gt` query param

        response_gt_rate_place = self.client.get('/api/leaderboard/?rate_place__gt=5')
        response_dict = json.loads(response_gt_rate_place.content)
        for rec in response_dict['results']:
            self.assertTrue(rec['rate_place'] > 5)

        response_gte_rate_place = self.client.get('/api/leaderboard/?rate_place__gte=5')
        response_dict = json.loads(response_gte_rate_place.content)
        for rec in response_dict['results']:
            self.assertTrue(rec['rate_place'] >= 5)

        response_exact_user_id = self.client.get('/api/leaderboard/?user_id=150')
        response_dict = json.loads(response_exact_user_id.content)
        self.assertEqual(response_dict['results'][0]['user_id'], 150)
        self.assertEqual(len(response_dict['results']), 1)
