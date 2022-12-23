import unittest
from Bot.py import check, check_adm, number


class messageTest(unittest.TestCase):
    def test_1(self):
        self.assertEqual(check('инцел'), 1)

    def test_2(self):
        self.assertEqual(check('воробушек'), 0)

    def test_3(self):
        self.assertEqual(check('Не Гр'), 1)

    def test_bd(self):
        self.assertEqual(int(check_adm('ruslane2091#6184')), 1)

    def test_bd2(self):
        self.assertEqual(int(check_adm('User1234#1111')), 0)

    def test_emoji(self):
        self.assertEqual(str(number('👍')), 0)


if __name__ == "__main__":
    unittest.main()
