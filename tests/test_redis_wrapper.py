import unittest
from mock import patch

from ewx_url_shortener.model.redis_wrapper import RedisWrapper


class RedisWrapperTest(unittest.TestCase):

    @patch("redis.Redis")
    def test_convert_redis_value_to_dict(self, redis_mock):
        rw = RedisWrapper()
        test_value = ''.join(['shortcode:qwe123,created:2021-01-10T20:45:00.000Z,',
                              'lastRedirect:2021-01-11T20:45:00.000Z,redirectCount:1'])
        test_dict = {
            'shortcode': 'qwe123',
            'created': '2021-01-10T20:45:00.000Z',
            'lastRedirect': '2021-01-11T20:45:00.000Z',
            'redirectCount': '1'
        }

        result = rw.convert_redis_value_to_dict(test_value)
        self.assertEqual(test_dict['shortcode'], result['shortcode'])
        self.assertEqual(test_dict['created'], result['created'])
        self.assertEqual(test_dict['lastRedirect'], result['lastRedirect'])
        self.assertEqual(test_dict['redirectCount'], result['redirectCount'])

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


