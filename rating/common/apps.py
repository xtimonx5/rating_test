from django.apps import AppConfig
from django.conf import settings


class CommonConfig(AppConfig):
    name = 'common'

    def ready(self):
        from .consumer import AMQPConsumer  # to be imported when apps are ready
        from .crontab import RefreshMVCrontab  # ^

        cron = RefreshMVCrontab()

        if not settings.TESTING:
            consumer = AMQPConsumer()
            consumer.daemon = True
            consumer.start()

        if not settings.TESTING:
            cron.configure_job()
            cron.run(interval=1)
