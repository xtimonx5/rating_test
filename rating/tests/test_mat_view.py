from django.test import TestCase
from common.models import RateRecord, LeaderBoard
from datetime import timedelta, datetime
from .common import CommonRatingTest


class MaterializedViewBuildingTestCase(CommonRatingTest):
    """
    tests that materialized view builds leaderboard 
    """

    def test_building_by_datetime(self):
        rec1 = RateRecord.objects.create(user_id=10, rating=1.5, datetime=datetime.now())
        rec2 = RateRecord.objects.create(user_id=11, rating=1.5, datetime=datetime.now() + timedelta(seconds=5))
        self._refresh_mat_view()

        leaderboard_rec1 = LeaderBoard.objects.first()
        self.assertEqual(leaderboard_rec1.user_id, rec1.user_id)
        leaderboard_rec2 = LeaderBoard.objects.last()
        self.assertEqual(leaderboard_rec2.user_id, rec2.user_id)

    def test_building_by_rating(self):
        rec1 = RateRecord.objects.create(user_id=10, rating=1.5, datetime=datetime.now())
        rec2 = RateRecord.objects.create(user_id=11, rating=2, datetime=datetime.now() + timedelta(seconds=5))
        self._refresh_mat_view()

        leaderboard_rec1 = LeaderBoard.objects.first()
        self.assertEqual(leaderboard_rec1.user_id, rec2.user_id)
        leaderboard_rec2 = LeaderBoard.objects.last()
        self.assertEqual(leaderboard_rec2.user_id, rec1.user_id)

    def test_rebuilding_places(self):
        rec1 = RateRecord.objects.create(user_id=10, rating=1.5, datetime=datetime.now())
        rec2 = RateRecord.objects.create(user_id=11, rating=2, datetime=datetime.now() + timedelta(seconds=5))
        self._refresh_mat_view()

        leaderboard_rec1 = LeaderBoard.objects.first()
        self.assertEqual(leaderboard_rec1.user_id, rec2.user_id)
        leaderboard_rec2 = LeaderBoard.objects.last()
        self.assertEqual(leaderboard_rec2.user_id, rec1.user_id)

        rec1.rating = 3
        rec1.save()
        self._refresh_mat_view()

        leaderboard_rec1 = LeaderBoard.objects.first()
        self.assertEqual(leaderboard_rec1.user_id, rec1.user_id)
        leaderboard_rec2 = LeaderBoard.objects.last()
        self.assertEqual(leaderboard_rec2.user_id, rec2.user_id)