import json
import threading

import pika
from django.conf import settings

from common.api.serializers.rate_record import AMQPMessageSerializer


class AMQPConsumer(threading.Thread):
    def message_handler(self, channel, method, properties, body):
        data = json.loads(body)
        serializer = AMQPMessageSerializer(data=data)
        serializer.process()

    @staticmethod
    def _get_connection():
        credentials = pika.PlainCredentials('user', 'password')
        parameters = pika.ConnectionParameters(host=settings.AMQP_HOST, credentials=credentials)
        return pika.BlockingConnection(parameters)

    def run(self):
        try:
            connection = self._get_connection()
        except:
            from time import sleep
            sleep(1)
            print('rabbimq is not listening. waiting')
            self.run()
        channel = connection.channel()

        channel.queue_declare(queue=settings.QUEUE_NAME)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(on_message_callback=self.message_handler, queue=settings.QUEUE_NAME, auto_ack=True)
        channel.start_consuming()
