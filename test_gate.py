# Unit tests for bitshares-indicator
# https://github.com/happyconcepts/bitshares-indicator
# bitshares-indicator copyright 2018 ben bird

# python -m unittest test_gate

import unittest
import bitshares_indicator

class TestBitSharesIndicator(unittest.TestCase):

    def setUpModule():

	print ("in setUpModule()")

    def test_Add(self):
	result = bitshares_indicator.add(10,5)
	self.assertEqual(result, 15)

    def test_Gate(self):
	g = bitshares_indicator.gate()
	result = g.run()
	self.assertTrue(result)
	#self.assertEqual(result, "No JSON object could be decoded")

if __name__ == '__main__':
    unittest.main()

