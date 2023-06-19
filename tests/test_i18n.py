import unittest
from drawzero.utils.i18n import I18N


class TestLangChange(unittest.TestCase):
    def test_ru(self):
        I18N.set_lang('ru')
        self.assertEqual(I18N.dummy, 'dummy_ru')

    def test_en(self):
        I18N.set_lang('en')
        self.assertEqual(I18N.dummy, 'dummy_en')


if __name__ == "__main__":
    unittest.main()
