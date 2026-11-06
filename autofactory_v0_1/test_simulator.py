import unittest
from simulator import Shift, metrics, simulate

class TestFactory(unittest.TestCase):
    def test_perfect(self):
        self.assertAlmostEqual(metrics(Shift(60, 0, 60, 60, 60))['oee'], 1)
    def test_known(self):
        self.assertAlmostEqual(metrics(Shift(100, 20, 60, 64, 60))['oee'], .6)
    def test_reproducible(self):
        self.assertEqual(simulate(), simulate())
    def test_bounds(self):
        self.assertTrue(all(0 <= x['oee'] <= 1 for x in simulate()))
    def test_invalid(self):
        with self.assertRaises(ValueError): metrics(Shift(60, 60, 60, 10, 9))

if __name__ == '__main__': unittest.main()
