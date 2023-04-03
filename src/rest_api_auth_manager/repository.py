import logging
from redis import Redis, BlockingConnectionPool, exceptions
import json


class CredentialsDatabase:

    def __init__(self, host: str, username: str = None, password: str = None, port: int = 6379) -> None:
        self.host = host
        self.port = port

        logging.info(f"Trying to connect with redis server: {self.host}")
        self.conn = Redis(connection_pool=BlockingConnectionPool(
            max_connections=20,
            timeout=10,
            host=self.host,
            username=username,
            password=password,
            port=port,
            db=0)
        )

        self.is_alive()

    def is_alive(self) -> bool:
        try:
            self.conn.ping()
            logging.info(f"Connection estabilished: {self.host}")
            return True
        except exceptions.ConnectionError:
            logging.error(f"Could not connect with host: {self.host}")
            return False

    def insert(self, key, value):
        logging.info(f"Inserting key {key}")
        self.conn.hmset(key, value)
        logging.debug(f"Key {key} inserted with success")

    def insert_hash(self, hash_name, key, value):
        logging.info(f"Inserting key {key}")
        self.conn.hset(hash_name, key, value)
        logging.debug(f"Key {key} inserted with success")

    def hget_all(self, key, default=None):
        value = self.conn.hgetall(key)
        if value:
            logging.debug(f"Key {key} Found")
            return value

        logging.debug(f"Key {key} not found")

        if default is not None:
            logging.debug("Returning default value")
            return default

    def hget(self, hash: str, key: str, default=None):
        value = self.conn.hget(hash, key)
        if value:
            logging.debug(f"Key {key} Found")
            return value

        logging.debug(f"Key {key} not found")

        if default is not None:
            logging.debug("Returning default value")
            return default

    def get_user(self, user_name):
        user = self.hget("USERS", user_name)
        if user:
            return json.loads(user.decode())

    def get_resources_map(self):
        rmap = self.hget_all("RESOURCES_MAP", default=dict())
        if rmap:
            for k, v in rmap.copy().items():
                rmap[k.decode()] = v.decode()
                rmap.pop(k)
            return rmap
        return {}
