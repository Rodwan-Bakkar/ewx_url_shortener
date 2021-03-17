
import unittest
from mock import MagicMock

from ewx_url_shortener.core.short_code_generator import ShortCodeGenerator
from ewx_url_shortener.model.redis_wrapper import RedisWrapper


class ShortCodeGeneratorTest(unittest.TestCase):
    NUMBERS = '0123456789'
    ENGLISH_SMALL_LETTERS = 'abcdefijklmnopqrstuvwxyz'
    ENGLISH_CAPITAL_LETTERS = 'ABCDEFIJKLMNOPQRSTUVWXYZZ'
    UNDERSCORE = '_'
    SHORT_CODE_CHARACTERS_RANGE = '{}{}{}{}'.format(
        NUMBERS,
        ENGLISH_SMALL_LETTERS,
        ENGLISH_CAPITAL_LETTERS,
        UNDERSCORE
    )

    SHORT_CODE_LENGTH = 6

    def test_generate_short_code(self):
        redis_wrapper_mocked = MagicMock(specset=RedisWrapper)
        redis_wrapper_mocked.short_code_exists.return_value = False
        scg = ShortCodeGenerator(redis_wrapper_mocked)
        short_code = scg.generate_short_code()
        self.assertEqual(self.SHORT_CODE_LENGTH, len(short_code))
        for ch in short_code:
            self.assertEqual(True, ch in self.SHORT_CODE_CHARACTERS_RANGE)

    def test_validate_short_code_correct(self):
        scg = ShortCodeGenerator(None)
        correct_short_code = '123_er'
        result = scg.validate_short_code(correct_short_code)
        self.assertEqual(True, result)

    def test_validate_short_code_wrong(self):
        scg = ShortCodeGenerator(None)
        wrong_short_code = '123_e&'
        result = scg.validate_short_code(wrong_short_code)
        self.assertEqual(False, result)

