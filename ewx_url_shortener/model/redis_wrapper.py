
import redis
import datetime

from ewx_url_shortener.model import StorageBase


class RedisWrapper(StorageBase):

    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    # TODO: include milliseconds
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
        now_iso = datetime.datetime.now()
        now_iso_str = now_iso.strftime(self.DATE_FORMAT)
        created = now_iso_str
        last_redirect = now_iso_str
        redirect_count = 0
        value_to_store = 'shortcode:{},created:{},lastRedirect:{},redirectCount:{}'.format(
            short_code,
            created,
            last_redirect,
            redirect_count
        )
        self._redis.set(url, value_to_store)

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
        return self._redis.get(url)

