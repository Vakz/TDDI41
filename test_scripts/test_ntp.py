#! /usr/bin/python3

import subprocess
import sys
import unittest

class NTPTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        hostname_call = subprocess.Popen(["hostname"], stdout=subprocess.PIPE)
        hostname = hostname_call.communicate()[0].strip().decode("utf-8")
        if (hostname_call.returncode != 0):
            print("Unable to get own hostname, exiting")
            sys.exit(1)
        if hostname == "gw":
            self.expectedSource = "ida-gw"
        else:
            self.expectedSource = "gw"

    def test_ntp(self):
        ntpq_call = subprocess.Popen(["ntpq", "-p"], stdout=subprocess.PIPE)
        ntpq_output = ntpq_call.communicate()[0].strip().decode("utf-8")
        result_row = ntpq_output.split("\n")[-1].split()
        source = result_row[0][1:].split('.')[0]
        reach = result_row[6]
        """
        This test fails a lot due to lag issues.
        It passes fine when the network works properly.
        """
        self.assertEqual(reach, "377")
        self.assertEqual(source, self.expectedSource)

if __name__ == '__main__':
    unittest.main()
