
from flask import jsonify

from ewx_url_shortener.core.http_responses import HTTPCodes

from ewx_url_shortener.core.errors import (
    ResponseError,
    URLNotPresentError,
    InvalidShortCodeError,
    ShortCodeAlreadyInUseError,
    ShortCodeNotFoundError
)


class RequestHandler:
    def __init__(self, scg, dbw):
        self.scg = scg
        self.dbw = dbw

    def shorten_url(self, request):
        """
        This function is to create (or to receive) a short code for a url and store
        the url and its short code in the database,
        It will also do the necessary validations for the code if provided
        Args:
            request(werkzeug.local.LocalProxy.Request): HTTP request
        Returns:
            tuple: a message with an http response code
        """
        url = request.args.get('url')
        short_code = request.args.get('short_code')

        try:
            if not url:
                raise URLNotPresentError('Url not present',
                                         HTTPCodes.CODE_400.value)
            elif self.dbw.url_already_exists(url):
                short_code = self.dbw.get_short_code_by_url(url)
                res_msg = {
                    'msg': 'url is already shortened',
                    'shortcode': short_code
                }
                return jsonify(res_msg), HTTPCodes.CODE_200.value

            if short_code:
                if not self.scg.validate_short_code(short_code):
                    raise InvalidShortCodeError('Invalid short code',
                                                HTTPCodes.CODE_412.value)
                elif self.dbw.short_code_exists(short_code):
                    raise ShortCodeAlreadyInUseError('Short code already in use',
                                                     HTTPCodes.CODE_412.value)
                else:
                    self.dbw.store_url(url, short_code)
                    res_msg = {
                        'shortcode': short_code
                    }
                    return jsonify(res_msg), HTTPCodes.CODE_201.value

            else:
                new_short_code = self.scg.generate_short_code()
                self.dbw.store_url(url, new_short_code)
                res_msg = {
                    'shortcode': new_short_code
                }
                return jsonify(res_msg), HTTPCodes.CODE_201.value
        except ResponseError as re:
            return re.msg, re.code

    def get_short_code(self, request):
        """
        This function is to check if short code exists in datastore and returns its info
        Args:
            request(werkzeug.local.LocalProxy.Request): HTTP request
        Returns:
            tuple: a message (short code info) with an http response code
        """
        short_code = request.args.get('short_code')
        url = self.dbw.short_code_exists(short_code)
        try:
            if url:
                short_code_info = self.dbw.get_short_code_info_by_url(url)
                short_code_info_dict = {item.split(':')[0]: item.split(':')[1]
                                        for item in short_code_info.split(',')}
                return jsonify(short_code_info_dict), HTTPCodes.CODE_302.value
            else:
                raise ShortCodeNotFoundError('Short code not found',
                                             HTTPCodes.CODE_404.value)
        except ShortCodeNotFoundError as scnfe:
            return scnfe.msg, scnfe.code

    def get_short_code_stats(self, request):
        """
        This function is to check if short code exists in datastore and returns its stats
        Args:
            request(werkzeug.local.LocalProxy.Request): HTTP request
        Returns:
            tuple: a message (short code stats) with an http response code
        """

        short_code = request.args.get('short_code')
        url = self.dbw.short_code_exists(short_code)
        try:
            if url:
                short_code_info = self.dbw.get_short_code_info_by_url(url)
                short_code_info_dict = {item.split(':')[0]: item.split(':')[1]
                                        for item in short_code_info.split(',')}
                return jsonify(short_code_info_dict), HTTPCodes.CODE_200.value
            else:
                raise ShortCodeNotFoundError('Short code not found',
                                             HTTPCodes.CODE_404.value)
        except ShortCodeNotFoundError as scnfe:
            return scnfe.msg, scnfe.code

