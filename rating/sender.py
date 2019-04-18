import json

import pika

MESSAGES_COUNT = 10000

credentials = pika.PlainCredentials('user', 'password')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq', credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='rating_message_queue')

from datetime import datetime, timedelta

import random


def gen_datetime(min_year=1900, max_year=datetime.now().year):
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()


now1 = datetime.now()


def get_random_body():
    dict_to_send = {
        'user_id': random.randint(1, 1000000000),
        'rating': random.uniform(1, 100000),
        'datetime': gen_datetime(1990).timestamp()
    }
    return json.dumps(dict_to_send)


[channel.basic_publish(exchange='', routing_key='rating_message_queue', body=get_random_body()) for x in
 range(MESSAGES_COUNT)]

print('{} microseconds was spend to send {} messages'.format((datetime.now() - now1).microseconds,
                                                             MESSAGES_COUNT))

connection.close()
