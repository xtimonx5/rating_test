import logging
from datetime import datetime

from django.utils.timezone import now
from rest_framework import serializers

from common.models import RateRecord, LeaderBoard

logger = logging.getLogger('amqp')


class AMQPMessageSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    rating = serializers.FloatField(required=True)
    datetime = serializers.DateTimeField(required=False, default=now)

    def is_valid(self, raise_exception=False):
        datetime_obj = datetime.utcfromtimestamp(self.initial_data['datetime']).strftime('%Y-%m-%d %H:%M:%S')
        self.initial_data['datetime'] = datetime_obj
        super(AMQPMessageSerializer, self).is_valid()

    def process(self):
        if self.is_valid():
            logger.error(f'{self.initial_data} is not valid. Passed')
        else:
            RateRecord.objects.update_or_create(
                user_id=self.validated_data['user_id'],
                defaults=self.validated_data
            )


class LeaderBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaderBoard
        fields = '__all__'
