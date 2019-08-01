import json
from redbeat import RedBeatScheduler
from redbeat.schedulers import get_redis
from celery.utils.log import get_logger
import redis.exceptions

logger = get_logger(__name__)

class ItsdownRedBeatScheduler(RedBeatScheduler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_periodic_tasks(self):
        logger.debug('Getting periodic tasks from Redis')

        client = get_redis(self.app)
        entries = {}
        for k in client.scan_iter('redbeat:*'):
            if 'backend_cleanup' in k:
                continue
            try:
                entries[k] = json.loads(client.hget(k, 'definition'))
            except redis.exceptions.ResponseError as e:
                logger.debug(
                    f"Value of hash: '{k}' is not a periodic task entry"
                )

        return entries

    def remove_periodic_task(self, key):
        logger.debug('Getting periodic tasks from Redis')

        client = get_redis(self.app)
        try:
            rv = client.delete(key)
        except Exception as e:
            logger.debug(
                f"Could not delete entry with key: '{key}'"
            )
            rv = 0

        return rv


