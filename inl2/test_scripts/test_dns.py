#! /usr/bin/python3

import subprocess
import sys
import unittest

class Host:
    def __init__(self, hostname, ip):
        self.hostname = hostname
        self.ip = ip


class DNSTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.domain = ".d1.sysinst.ida.liu.se"
        hostname_call = subprocess.Popen(["hostname"], stdout=subprocess.PIPE)
        self.hostname = hostname_call.communicate()[0].strip().decode("utf-8")
        if (hostname_call.returncode != 0):
            print("Unable to get own hostname, exiting")
            sys.exit(1)

        ip_call = subprocess.Popen(["hostname", "--ip-address"], stdout=subprocess.PIPE)
        self.ip = ip_call.communicate()[0].strip().decode("utf-8")
        if (ip_call.returncode != 0):
            print("Unable to get own ip, exiting")
            sys.exit(1)

        self.hosts = [
            Host("gw", "130.236.179.66"),
            Host("client-1", "130.236.179.67"),
            Host("client-2", "130.236.179.68"),
            Host("server", "130.236.179.69")
            ]

    def test_name_resolution(self):
        for host in self.hosts:
            if host.hostname == self.hostname:
                continue
            ip_call = subprocess.Popen(["host", host.hostname + self.domain], stdout=subprocess.PIPE)
            ip = ip_call.communicate()[0].strip().decode("utf-8").split()[-1]
            self.assertEqual(ip, host.ip)

    def test_reverse_dns(self):
        for host in self.hosts:
            if host.hostname == self.hostname:
                continue
            reverse_call = subprocess.Popen(["dig", "+short", "-x", host.ip], stdout=subprocess.PIPE)
            hostname = reverse_call.communicate()[0].strip().decode("utf-8").split('\n')[-1].split('.')[0]
            self.assertEqual(hostname, host.hostname)

if __name__ == '__main__':
    unittest.main()
