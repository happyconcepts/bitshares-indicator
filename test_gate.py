# Testing module for bitshares-indicator
# test_gate.py
# bitshares-indicator copyright 2018 ben bird
# https://github.com/happyconcepts/bitshares-indicator
# mit license ~ open source software 

# python -m unittest test_gate.py
# import unittest module 9in std 
import unittest
import bitshares-indicator

class TestCalc(unittest.TestCase):

    def testGate(self):
	result = bitshares-indicator.add(10,5)
	self.assertEqual(result, 15)


