from redis import Redis

from .config import Config

global_config = Config()

redis = Redis(host=global_config.redis.host, port=global_config.redis.port)
