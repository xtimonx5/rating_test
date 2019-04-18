from crontab import CronTab
from django.conf import settings


class RefreshMVCrontab(object):
    def __init__(self):
        self.cron = CronTab(user='django')
        self.cron.remove_all()

    def configure_job(self):
        self.job = self.cron.new(
            command=f"/usr/bin/psql -U {settings.DB_USER} -h {settings.DB_HOST} -d {settings.DB_NAME} -p {settings.DB_PORT} -c 'SELECT refresh_leaderboard_mv();'")

    def run(self, interval=1):
        """
        :param interval: interval to run crontab (minutes) 
        :return: 
        """
        self.job.minute.every(interval)
        self.job.enable()

        self.cron.write()
