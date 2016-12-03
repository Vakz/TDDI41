#! /usr/bin/python3

import unittest
import test_networking
import test_dns

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(test_networking))
suite.addTests(loader.loadTestsFromModule(test_dns))

runner = unittest.TextTestRunner(verbosity=3)
runner.run(suite)
