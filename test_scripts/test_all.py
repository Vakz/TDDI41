#! /usr/bin/python3

import unittest
import test_networking
import test_dns
import test_ntp
import test_nis
import test_nfs

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(test_networking))
suite.addTests(loader.loadTestsFromModule(test_dns))
suite.addTests(loader.loadTestsFromModule(test_ntp))
suite.addTests(loader.loadTestsFromModule(test_nis))
suite.addTests(loader.loadTestsFromModule(test_nfs))

runner = unittest.TextTestRunner(verbosity=3)
runner.run(suite)
