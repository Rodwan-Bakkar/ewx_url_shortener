import unittest
from mock import MagicMock
from flask import Flask

from werkzeug.local import LocalProxy

from ewx_url_shortener.core.request_handler import RequestHandler
from ewx_url_shortener.core.short_code_generator import ShortCodeGenerator
from ewx_url_shortener.model.redis_wrapper import RedisWrapper


class RequestHandlerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        setting app a context for the flask app to be
        able to use jsonify inside a flask context
        """
        app = Flask(__name__)
        app.config['SERVER_NAME'] = 'localhost:5000'
        cls.client = app.test_client()
        app_context = app.app_context()
        app_context.push()

    def test_shorten_url_no_url(self):
        redis_wrapper_mocked = MagicMock(specset=RedisWrapper)
        short_code_generator_mocked = MagicMock(specset=ShortCodeGenerator)
        request_mocked = MagicMock(specset=LocalProxy)
        scg = RequestHandler(short_code_generator_mocked, redis_wrapper_mocked)

        request_mocked.args = {}

        result = scg.shorten_url(request_mocked)
        self.assertEqual('Url not present', result[0])
        self.assertEqual(400, result[1])

    def test_shorten_url_url_already_exists(self):
        redis_wrapper_mocked = MagicMock(specset=RedisWrapper)
        short_code_generator_mocked = MagicMock(specset=ShortCodeGenerator)
        request_mocked = MagicMock(specset=LocalProxy)
        redis_wrapper_mocked.get_short_code_by_url.return_value = 'qwe123'
        redis_wrapper_mocked.url_already_exists.return_value = True
        scg = RequestHandler(short_code_generator_mocked, redis_wrapper_mocked)

        request_mocked.args = {
            'url': 'test_url_which_is_already_shortened'
        }

        result = scg.shorten_url(request_mocked)
        self.assertEqual('url is already shortened', result[0].json['msg'])
        self.assertEqual('qwe123', result[0].json['shortcode'])
        self.assertEqual(200, result[1])

    def test_shorten_url_url_does_not_exists_short_code_wrong(self):
        redis_wrapper_mocked = MagicMock(specset=RedisWrapper)
        short_code_generator_mocked = MagicMock(specset=ShortCodeGenerator)
        request_mocked = MagicMock(specset=LocalProxy)
        redis_wrapper_mocked.get_short_code_by_url.return_value = 'qwe123'
        redis_wrapper_mocked.url_already_exists.return_value = False
        short_code_generator_mocked.validate_short_code.return_value = False
        scg = RequestHandler(short_code_generator_mocked, redis_wrapper_mocked)

        request_mocked.args = {
            'url': 'test_url_which_is_not_yet_shortened',
            'short_code': 'qwe123'
        }

        result = scg.shorten_url(request_mocked)
        self.assertEqual('Invalid short code', result[0])
        self.assertEqual(412, result[1])

    def test_shorten_url_url_does_not_exists_short_code_correct_and_already_in_use(self):
        redis_wrapper_mocked = MagicMock(specset=RedisWrapper)
        short_code_generator_mocked = MagicMock(specset=ShortCodeGenerator)
        request_mocked = MagicMock(specset=LocalProxy)
        redis_wrapper_mocked.get_short_code_by_url.return_value = 'qwe123'
        redis_wrapper_mocked.url_already_exists.return_value = False
        short_code_generator_mocked.validate_short_code.return_value = True
        redis_wrapper_mocked.short_code_exists.return_value = True

        scg = RequestHandler(short_code_generator_mocked, redis_wrapper_mocked)

        request_mocked.args = {
            'url': 'test_url_which_is_not_yet_shortened',
            'short_code': 'qwe123'
        }

        result = scg.shorten_url(request_mocked)
        self.assertEqual('Short code already in use', result[0])
        self.assertEqual(412, result[1])

    def test_shorten_url_url_does_not_exists_short_code_correct_and_not_in_use(self):
        redis_wrapper_mocked = MagicMock(specset=RedisWrapper)
        short_code_generator_mocked = MagicMock(specset=ShortCodeGenerator)
        request_mocked = MagicMock(specset=LocalProxy)

        redis_wrapper_mocked.get_short_code_by_url.return_value = 'qwe123'
        redis_wrapper_mocked.url_already_exists.return_value = False
        redis_wrapper_mocked.short_code_exists.return_value = False
        short_code_generator_mocked.validate_short_code.return_value = True

        scg = RequestHandler(short_code_generator_mocked, redis_wrapper_mocked)

        request_mocked.args = {
            'url': 'test_url_which_is_not_yet_shortened',
            'short_code': 'qwe123'
        }

        result = scg.shorten_url(request_mocked)
        self.assertEqual('qwe123', result[0].json['shortcode'])
        self.assertEqual(201, result[1])

    def test_shorten_url_url_does_not_exists_short_code_not_provided(self):
        redis_wrapper_mocked = MagicMock(specset=RedisWrapper)
        short_code_generator_mocked = MagicMock(specset=ShortCodeGenerator)
        request_mocked = MagicMock(specset=LocalProxy)

        redis_wrapper_mocked.url_already_exists.return_value = False
        short_code_generator_mocked.generate_short_code.return_value = 'qwe123'

        scg = RequestHandler(short_code_generator_mocked, redis_wrapper_mocked)

        request_mocked.args = {
            'url': 'test_url_which_is_not_yet_shortened',
        }

        result = scg.shorten_url(request_mocked)
        self.assertEqual('qwe123', result[0].json['shortcode'])
        self.assertEqual(201, result[1])

    def test_get_short_code_does_not_exist(self):
        redis_wrapper_mocked = MagicMock(specset=RedisWrapper)
        short_code_generator_mocked = MagicMock(specset=ShortCodeGenerator)
        request_mocked = MagicMock(specset=LocalProxy)

        redis_wrapper_mocked.short_code_exists.return_value = None

        scg = RequestHandler(short_code_generator_mocked, redis_wrapper_mocked)

        request_mocked.args = {
            'short_code': 'qwe123'
        }

        result = scg.get_short_code(request_mocked)
        self.assertEqual('Short code not found', result[0])
        self.assertEqual(404, result[1])

    def test_get_short_code_exists(self):
        redis_wrapper_mocked = MagicMock(specset=RedisWrapper)
        short_code_generator_mocked = MagicMock(specset=ShortCodeGenerator)
        request_mocked = MagicMock(specset=LocalProxy)

        redis_wrapper_mocked.short_code_exists.return_value = 'test_url'
        redis_wrapper_mocked.get_short_code_info_by_url.return_value = {
            'shortcode': 'qwe123',
            'created': '2021-01-10T20:45:00.000Z',
            'lastRedirect': '2021-01-11T20:45:00.000Z',
            'redirectCount': 1
        }

        scg = RequestHandler(short_code_generator_mocked, redis_wrapper_mocked)

        request_mocked.args = {
            'short_code': 'qwe123'
        }

        result = scg.get_short_code(request_mocked)
        self.assertEqual('qwe123', result[0].json['shortcode'])
        self.assertEqual('2021-01-10T20:45:00.000Z', result[0].json['created'])
        self.assertEqual('2021-01-11T20:45:00.000Z', result[0].json['lastRedirect'])
        self.assertEqual(1, result[0].json['redirectCount'])
        self.assertEqual(302, result[1])

    # def test_get_short_code_stats_short_code_does_not_exit(self):
    #     redis_wrapper_mocked = MagicMock(specset=RedisWrapper)
    #     short_code_generator_mocked = MagicMock(specset=ShortCodeGenerator)
    #     request_mocked = MagicMock(specset=LocalProxy)
    #
    #     redis_wrapper_mocked.short_code_exists.return_value = None
    #
    #     scg = RequestHandler(short_code_generator_mocked, redis_wrapper_mocked)
    #
    #     request_mocked.args = {
    #         'short_code': 'qwe123'
    #     }
    #
    #     result = scg.get_short_code(request_mocked)
    #     self.assertEqual('Short code not found', result[0])
    #     self.assertEqual(404, result[1])
    #
    # def test_get_short_code_stats_short_code_exists(self):
    #     redis_wrapper_mocked = MagicMock(specset=RedisWrapper)
    #     short_code_generator_mocked = MagicMock(specset=ShortCodeGenerator)
    #     request_mocked = MagicMock(specset=LocalProxy)
    #
    #     redis_wrapper_mocked.short_code_exists.return_value = 'test_url'
    #     redis_wrapper_mocked.get_short_code_info_by_url.return_value = {
    #         'shortcode': 'qwe123',
    #         'created': '2021-01-10T20:45:00.000Z',
    #         'lastRedirect': '2021-01-11T20:45:00.000Z',
    #         'redirectCount': 1
    #     }
    #
    #     scg = RequestHandler(short_code_generator_mocked, redis_wrapper_mocked)
    #
    #     request_mocked.args = {
    #         'short_code': 'qwe123'
    #     }
    #
    #     result = scg.get_short_code(request_mocked)
    #     self.assertEqual('qwe123', result[0].json['shortcode'])
    #     self.assertEqual('2021-01-10T20:45:00.000Z', result[0].json['created'])
    #     self.assertEqual('2021-01-11T20:45:00.000Z', result[0].json['lastRedirect'])
    #     self.assertEqual(1, result[0].json['redirectCount'])
    #     self.assertEqual(302, result[1])



