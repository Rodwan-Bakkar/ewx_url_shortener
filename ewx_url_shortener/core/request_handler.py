
from flask import jsonify

from ewx_url_shortener.core.http_responses import HTTPCodes

from ewx_url_shortener.core.errors import (
    ResponseError,
    URLNotPresentError,
    InvalidShortCodeError,
    ShortCodeAlreadyInUseError
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
                # TODO: get the short code from databse
                short_code = 'XXXXXX'
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

    def get_short_code(self):
        """
        This function is to *****
        Args:
        Returns:
            tuple: a message with an http response code
        """
        pass

    def get_short_code_stats(self):
        """
        This function is to *****
        Args:
        Returns:
            tuple: a message with an http response code
        """

        res_msg = {
            'created': '',
            'lastRedirect': '',
            'redirectCount': '',
        }

        return jsonify(res_msg), HTTPCodes.CODE_200.value

