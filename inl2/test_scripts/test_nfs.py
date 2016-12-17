#! /usr/bin/python3

import subprocess
import sys
import unittest

class NFSTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.domain = ".d1.sysinst.ida.liu.se"
        hostname_call = subprocess.Popen(["hostname"], stdout=subprocess.PIPE)
        self.hostname = hostname_call.communicate()[0].strip().decode("utf-8")
        if (hostname_call.returncode != 0):
            print("Unable to get own hostname, exiting")
            sys.exit(1)
        self.userdirs = [("user1", "/home1/user1", "/home/user1"), ("user2", "/home2/user2", "/home/user2")]

    def check_mount_list(self, mounts, mount_path, mount_point):
        for mount in mounts:
            attributes = mount.split()
            # If mounting from correct path, and to the correct mount point, it's correctly mounted
            if (attributes[0] == mount_path and attributes[-1] == mount_point): return True
        return False

    def test_usr_local(self):
        # Only doing this test on clients
        path = "/usr/local"
        if (self.hostname not in ["client-1", ["client-2"]]): return
        df_call = subprocess.Popen(["df", "-h", "-P"], stdout=subprocess.PIPE)
        mounts = df_call.communicate()[0].strip().decode("utf-8").split("\n")
        found_mount = self.check_mount_list(mounts, "server%s:%s" % (self.domain, path), path)
        self.assertTrue(found_mount)




    def test_home_dirs(self):
        """
        This test will require the server to have uploaded its public key to both clients and both users,
        with no passphrase. See ssh-keygen and ssh-copy-id.
        Since the public keys are uploaded to the home directory of a user, which is mounted by the automounter,
        we technically know it works by the simple fact that we can log in with the ssh key at all, but we might
        as well check the mounts with df -h
        """
        # This is only to run on the server
        if (self.hostname != "server"): return
        for client in ["client-1", "client-2"]:
            for user in self.userdirs:
                expected_mount_path = "server%s:%s" % (self.domain, user[1])
                login = "%s@%s%s" % (user[0], client, self.domain)
                df_call = subprocess.Popen(["ssh", login, "df -h -P"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                mounts = df_call.communicate()[0].strip().decode("utf-8").split("\n")
                found_mount = self.check_mount_list(mounts, expected_mount_path, user[2])
                self.assertTrue(found_mount)

if __name__ == '__main__':
    unittest.main()
