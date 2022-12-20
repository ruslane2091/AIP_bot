import unittest
from CREED_bot import check


class messageTest(unittest.TestCase):
    def test_1(self):
        self.assertEqual(check(['инцел']), 1)
    
    def test_2(self):
        self.assertEqual(check(['воробушек']), 0)
    
    def test_3(self):
        self.assertEqual(check(['Не Гр']), 1)

if __name__ == "__main__":
    unittest.main()