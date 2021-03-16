
from flask import Flask, request

from ewx_url_shortener.core.short_code_generator import ShortCodeGenerator
from ewx_url_shortener.core.request_handler import RequestHandler
from ewx_url_shortener.model.database_wrapper import DatabaseWrapper


app = Flask(__name__)

scg = ShortCodeGenerator()
dbw = DatabaseWrapper()
rh = RequestHandler(scg, dbw)


@app.route('/shorten', methods=["POST"])
def shorten_url():
    """
    This function is to create (or to receive) a short code for a url and store
    the url and its short code in the database,
    It will also do the necessary validations for the code if provided
    Args:
    Returns:
        tuple: a message with an http response code
    """
    return rh.shorten_url(request)


@app.route('/<shortcode>', methods=["GET"])
def get_short_code():
    """
    This function is to *****
    Args:
    Returns:
        tuple: a message with an http response code
    """
    return rh.get_short_code()


@app.route('/<shortcode>/stats', methods=["GET"])
def get_short_code_stats():
    """
    This function is to *****
    Args:
    Returns:
        tuple: a message with an http response code
    """
    return rh.get_short_code_stats()


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
