Application is accepting amqp messages in `rating_message_queue`  queue. 
(Can be changed in settings), building PostgreSQL materialized view with rate place. 
Materialized view refreshes every minute.



To run application:
1. clone this repo
2. make `docker-compose build`
3. make `docker-compose up` (default env variables will run django runserver)


Allowed endpoints:

1. `127.0.0.1:8000/api/leaderboard/` - paginated leaderboard.

    allowed query_params:
     
        1.1`?rate_place=N`, - concrete rate place (N) 
        
        1.2`?rate_place__gt=N` - rate place greater than N
        
        1.3`?rate_place__gte=N` - rate place greater or equal to N
        
        1.4.`?rate_place__lt=N` - rate place lower than N
        
        1.5.`?rate_place__lte=N` - rate place lower or equal to N
        
        1.6.`?user_id=N` - user id is N
 
 
2. `127.0.0.1/api/leaderboard/${N}` - To find who is on N place and also it's "neighbors" 




Make commands (execute from base dir or project)

1. `make show_queue` - show queues in rabbitmq

2. `make test` - run unit tests

3. `make run_sender` - run simple rabbitmq message sender for 10000 messages. (just for developer test)