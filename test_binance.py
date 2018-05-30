# Unit tests for bitshares-indicator
# https://github.com/happyconcepts/bitshares-indicator
# bitshares-indicator copyright 2018 ben bird

# python -m unittest test_binance

import unittest
import bitshares_indicator

class TestBitSharesIndicator(unittest.TestCase):

    def setUpModule():
	print ("in setUpModule()")

    def test_Add(self):
	result = bitshares_indicator.add(10,5)
	self.assertEqual(result, 15)

    def test_Binance(self):
	b = bitshares_indicator.binance()
	result = b.run()
	self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
