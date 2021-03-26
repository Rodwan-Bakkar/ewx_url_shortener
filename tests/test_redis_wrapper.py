import unittest
from mock import MagicMock, patch
from flask import Flask

from werkzeug.local import LocalProxy

from ewx_url_shortener.core.request_handler import RequestHandler
from ewx_url_shortener.core.short_code_generator import ShortCodeGenerator
from ewx_url_shortener.model.redis_wrapper import RedisWrapper


class RedisWrapperTest(unittest.TestCase):
    def test_url_already_exists_yes(self):
        pass

    def test_url_already_exists_no(self):
        pass

    def test_store_url(self):
        pass

    def test_update_url_stats(self):
        pass

    def test_short_code_exists(self):
        pass

    def test_get_short_code_by_url(self):
        pass

    def test_get_short_code_info_by_url(self):
        pass

    @patch("redis.Redis")
    def test_convert_redis_value_to_dict(self):
        pass

    @patch("redis.Redis")
    def test_convert_dict_to_redis_value(self, redis_mock):
        rw = RedisWrapper()
        test_dict = {
            'shortcode': 'qwe123',
            'created': '2021-01-10T20:45:00.000Z',
            'lastRedirect': '2021-01-11T20:45:00.000Z',
            'redirectCount': 1
        }

        result = rw.convert_dict_to_redis_value(test_dict)
        self.assertEqual('shortcode:qwe123,created:2021-01-10T20:45:00.000Z,'
                         'lastRedirect:2021-01-11T20:45:00.000Z,redirectCount:1', result)


