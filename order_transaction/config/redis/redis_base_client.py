import redis
from set_path_config import *

redis_cli = redis.Redis(host=os.environ.get("REDIS_IP"), port=6379, decode_responses=True)