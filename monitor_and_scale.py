import redis
import subprocess
import time

REDIS_HOST = 'localhost'  # or 'redis' if running inside a container
REDIS_PORT = 6379
QUEUE_NAME = 'celery'
SCALE_THRESHOLD = 10  # Number of tasks in queue to trigger scaling
MAX_WORKERS = 5
MIN_WORKERS = 1
CHECK_INTERVAL = 10  # seconds

# The name of your docker-compose service for celery
CELERY_SERVICE = 'celery'


def get_queue_length():
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    return r.llen(QUEUE_NAME)

def get_current_workers():
    # Get the number of running celery containers
    result = subprocess.run([
        'docker-compose', 'ps', '-q', CELERY_SERVICE
    ], capture_output=True, text=True)
    return len([line for line in result.stdout.splitlines() if line.strip()])

def scale_workers(n):
    print(f"Scaling celery workers to {n}")
    subprocess.run([
        'docker-compose', 'up', '-d', '--scale', f'{CELERY_SERVICE}={n}'
    ])

def main():
    while True:
        queue_length = get_queue_length()
        current_workers = get_current_workers()
        print(f"Queue length: {queue_length}, Current workers: {current_workers}")

        if queue_length > SCALE_THRESHOLD and current_workers < MAX_WORKERS:
            scale_workers(current_workers + 1)
        elif queue_length == 0 and current_workers > MIN_WORKERS:
            scale_workers(current_workers - 1)
        # else: do nothing

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
