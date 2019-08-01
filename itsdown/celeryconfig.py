redis_host = '0.0.0.0'
redis_port = 6379

broker_url = f'redis://localhost:{redis_port}/5'
result_backend = f'redis://localhost:{redis_port}/6'

redbeat_redis_url = f'redis://localhost:{redis_port}/7'

beat_scheduler = 'redbeat.RedBeatScheduler'
beat_max_loop_interval = 1
redbeat_lock_timeout = 1

beat_schedule = {}
