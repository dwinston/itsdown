# Redis
redis_host = '0.0.0.0'
redis_port = 6379

# Celery
broker_url = f'redis://localhost:{redis_port}/5'
result_backend = f'redis://localhost:{redis_port}/6'

redbeat_redis_index = 7
redbeat_redis_url = f'redis://localhost:{redis_port}/{redbeat_redis_index}'

beat_scheduler = 'redbeat.RedBeatScheduler'
beat_max_loop_interval = 1
redbeat_lock_timeout = 1

beat_schedule = {}

# Flask
flask_port = 5000
flask_host = '0.0.0.0'
flask_url = f'{flask_host}:{flask_port}'
