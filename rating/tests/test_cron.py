from django.test import TestCase
from common.crontab import RefreshMVCrontab


class CronTabTestCase(TestCase):
    def test_crontab_adding(self):
        cron = RefreshMVCrontab()
        self.assertEqual(len(cron.cron.crons), 0)
        cron.configure_job()
        self.assertEqual(len(cron.cron.crons), 1)
        crontask = cron.cron.crons[0]
        self.assertIn('SELECT refresh_leaderboard_mv();', crontask.command)
