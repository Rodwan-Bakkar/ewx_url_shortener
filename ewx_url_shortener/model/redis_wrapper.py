
import redis
import datetime

from ewx_url_shortener.model import StorageBase


class RedisWrapper(StorageBase):

    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    # TODO: include milliseconds
    # TODO: should handle all redis exceptions
    DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.000Z'

    def __init__(self):
        self._redis = redis.Redis(
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            decode_responses=True
        )

    def url_already_exists(self, url):
        if self._redis.exists(url):
            return True
        return False

    def store_url(self, url, short_code):
        """
        This function is to store a URL and it's short code if the is URL
        is first time to be shortened

        Args:
            url(str): url
            short_code(str): short code
        Returns:
            None:
        """
        now_iso = datetime.datetime.now()
        now_iso_str = now_iso.strftime(self.DATE_FORMAT)
        created = now_iso_str
        last_redirect = now_iso_str
        redirect_count = 1
        value_to_store_dict = {
            'shortcode': short_code,
            'created': created,
            'lastRedirect': last_redirect,
            'redirectCount': redirect_count,
        }
        value_to_store = self.convert_dict_to_redis_value(value_to_store_dict)
        self._redis.set(url, value_to_store)

    def update_url_stats(self, url):
        """
        This function is to update the stats of URL if it already is shortened
        Args:
            url(str): url
        Returns:
            None:
        """
        redis_value = self._redis.get(url)
        redis_value_dict = self.convert_redis_value_to_dict(redis_value)

        now_iso = datetime.datetime.now()
        now_iso_str = now_iso.strftime(self.DATE_FORMAT)
        redis_value_dict['lastRedirect'] = now_iso_str

        redirect_count = int(redis_value_dict['redirectCount'])
        redis_value_dict['redirectCount'] = str(redirect_count+1)

        redis_value_updated = self.convert_dict_to_redis_value(redis_value_dict)

        self._redis.set(url, redis_value_updated)

    def short_code_exists(self, short_code):
        """
        This function is to check if the short code already exists in the datastore
        if the short code exists it will return the URL that was shortened to this code
        if the short code does not exists it will return None
        Args:
            short_code: short code to be validated
        Returns:
            str or None: it returns the URL in case the short code exists and None if it does not
        """
        for redis_key in self._redis.scan_iter("*"):
            redis_value = self._redis.get(redis_key)
            redis_short_code = redis_value.split(',')[0].split(':')[1]
            if short_code == redis_short_code:
                return redis_key

    def get_short_code_by_url(self, url):
        """
        This function is to get short code by url
        Args:
            url(str): the URL that already shortened
        Returns:
            str: the short code
        """
        redis_value = self._redis.get(url)
        short_code = redis_value.split(',')[0].split(':')[1]
        return short_code

    def get_short_code_info_by_url(self, url):
        """
        This function is to get the information of the URL
        this includes the time the URL was shortened,
        the last redirection time
        and the number of redirections

        Args:
            url(str): the URL that already shortened
        Returns:
            str: the information of the URL
        """
        redis_value = self._redis.get(url)
        redis_value_dict = self.convert_redis_value_to_dict(redis_value)
        return redis_value_dict

    @staticmethod
    def convert_redis_value_to_dict(redis_value):
        """
        This function is to convert a string redis value to a python dictionary
        Args:
            redis_value(str): the redis value in string format
        Returns:
            dict: the redis value in dictionary format
        """
        redis_value_dict = {
            item.split(':')[0]: item.split(':')[1]
            for item in redis_value.split(',')
        }
        return redis_value_dict

    @staticmethod
    def convert_dict_to_redis_value(redis_value_dict):
        """
        This function is to convert a python dictionary to a string redis value
        Args:
            redis_value_dict(dict): the redis value in python dictionary format
        Returns:
            str: the redis value in string format
        """
        redis_value_str = 'shortcode:{},created:{},lastRedirect:{},redirectCount:{}'.format(
            redis_value_dict['shortcode'],
            redis_value_dict['created'],
            redis_value_dict['lastRedirect'],
            redis_value_dict['redirectCount'],
        )
        return redis_value_str



