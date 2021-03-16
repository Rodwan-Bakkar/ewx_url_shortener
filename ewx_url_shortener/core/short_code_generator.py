
import random

from ewx_url_shortener.model.database_wrapper import DatabaseWrapper


class ShortCodeGenerator:

    NUMBERS = '0123456789'
    ENGLISH_SMALL_LETTERS = 'abcdeifjklmnopqrstuvwxyz'
    ENGLISH_CAPITAL_LETTERS = 'ABCDEFIJKLMNOPQRSTUVWXYZZ'
    UNDERSCORE = '_'
    SHORT_CODE_CHARACTERS_RANGE = '{}{}{}{}'.format(
        NUMBERS,
        ENGLISH_SMALL_LETTERS,
        ENGLISH_CAPITAL_LETTERS,
        UNDERSCORE
    )

    SHORT_CODE_LENGTH = 6

    def __init__(self):
        self.dbr = DatabaseWrapper()

    def generate_short_code(self):
        """
        This method is to generate a short code which was not already generated
        This short code is 6 characters and may only contain alphanumeric characters and underscores
        Args:
        Returns:
            str: a short code
        """
        while True:
            short_code_char_list = [random.choice(self.SHORT_CODE_CHARACTERS_RANGE)
                                    for _ in range(self.SHORT_CODE_LENGTH)]
            short_code = ''.join(short_code_char_list)
            if not self.dbr.short_code_exists(short_code):
                return short_code

    def validate_short_code(self, short_code):
        """
        This method is to validate a short code
        This short code must be 6 characters and may only contain alphanumeric characters and underscores
        Args:
            short_code: short code to be validated
        Returns:
            bool: if short code is valid or not
        """
        if len(short_code) != self.SHORT_CODE_LENGTH:
            return False
        for short_code_char in short_code:
            if short_code_char not in self.SHORT_CODE_CHARACTERS_RANGE:
                return False
        return True

