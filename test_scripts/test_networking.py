#! /usr/bin/python3

import subprocess
import sys
import unittest

class NetworkingTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.valid_hostnames = ["gw", "server", "client-1", "client-2"]
        self.addresses = [
            "google.com",
            "130.236.179.66",
            "130.236.179.67",
            "130.236.179.68",
            "130.236.179.69"
            ]

        ip_call = subprocess.Popen(["hostname", "--ip-address"], stdout=subprocess.PIPE)
        self.ip = ip_call.communicate()[0].strip().decode("utf-8")
        if (ip_call.returncode != 0):
            print("Unable to get own ip, exiting")
            sys.exit(1)

        hostname_call = subprocess.Popen(["hostname"], stdout=subprocess.PIPE)
        self.hostname = hostname_call.communicate()[0].strip().decode("utf-8")
        if (hostname_call.returncode != 0):
            print("Unable to get own hostname, exiting")
            sys.exit(1)

    def test_basic_networking(self):
        for destination in self.addresses:
            if (destination == self.ip):
                continue
            res = subprocess.Popen(["ping", "-c 1", "-W 6", destination], stdout=subprocess.PIPE)
            res.communicate()
            self.assertEqual(res.returncode, 0)

    def test_hostname(self):
        self.assertTrue(self.hostname in self.valid_hostnames)

    def test_routing_daemon(self):
        if (self.hostname != "gw"):
            # This test is only for the gateway
            return
        routing_call = subprocess.Popen(["nc", "-z", "localhost", "2602"], stdout=subprocess.PIPE)
        routing_call.communicate()
        self.assertEqual(routing_call.returncode, 0)

    if __name__ == '__main__':
        unittest.main()
