#! /usr/bin/python3

import subprocess
import sys
import unittest

class NISTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        hostname_call = subprocess.Popen(["hostname"], stdout=subprocess.PIPE)
        self.hostname = hostname_call.communicate()[0].strip().decode("utf-8")
        if (hostname_call.returncode != 0):
            print("Unable to get own hostname, exiting")
            sys.exit(1)
        if (self.hostname == "server"):
            self.expectedProcess = "ypserv"
            self.expectedYpwhich = "localhost"
        else:
            self.expectedProcess = "ypbind"
            self.expectedYpwhich = "server.d1.sysinst.ida.liu.se"

    # Check so the appropriate daemon is running. On server, should be ypserv. On client, should be ypbind
    def test_process_running(self):
        if (self.hostname == "gw"): return
        proc_call = subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE)
        proc_list = subprocess.Popen(["grep", self.expectedProcess], stdin=proc_call.stdout, stdout=subprocess.PIPE).communicate()[0].strip().decode("utf-8")
        proc_call.communicate() # Do this, or the process won't close and we get annoying warnings
        processes = proc_list.split("\n")
        for process in processes:
            # If the process isn't running, the list should probably just be empty, but do some simple checks to make sure we got the right process anyway.
            attributes = process.split()
            # If TTY is not "?", the process isn't a daemon, and it's not the process we're looking for. Might not be necessary, but might as well.
            if (attributes[6] != "?"): continue
            # Shouldn't even be in the list if it's not the proper process name, but lets make sure anyway
            # If the process was started as a daemon, it's listed as "/usr/sbin/<process>", but if it was started manually i.e. by user calling "ypbind", it's listed as just "ypbind", so check with #endswith
            self.assertTrue(attributes[10].endswith(self.expectedProcess))
            # If we got here, we've found that the process is running
            return
        self.assertTrue(False) # If we got here, process was not running, and the test failed

    # Check so we are bound to the correct server
    def test_server_ypwhich(self):
        if (self.hostname == "gw"): return
        ypwhich_call = subprocess.Popen(["ypwhich"], stdout=subprocess.PIPE)
        server = ypwhich_call.communicate()[0].strip().decode("utf-8")
        self.assertEqual(server, self.expectedYpwhich)

    # Check so the users are available
    def test_ypcat_passwd(self):
        if (self.hostname == "gw"): return
        users = subprocess.Popen(["ypcat", "passwd.byuid"],stdout=subprocess.PIPE).communicate()[0].strip().decode("utf-8").split()
        self.assertTrue(users[0].startswith("user1:"))
        self.assertTrue(users[1].startswith("user2:"))

if __name__ == '__main__':
    unittest.main()
