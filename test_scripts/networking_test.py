#! /usr/bin/python3

import subprocess
import sys

#testa routing
#nc -z localhost 2602

ip_call = subprocess.Popen(["hostname", "--ip-address"], stdout=subprocess.PIPE)
self_ip = ip_call.communicate()[0].strip().decode("utf-8")

if (ip_call.returncode != 0):
    print("Unable to get own ip, exiting")
    sys.exit(1)

addresses = [
    "google.com",
    "130.236.179.66",
    "130.236.179.67",
    "130.236.179.68",
    "130.236.179.69"
]

print("PING TESTS\n----------------------------------------------------")
for destination in addresses:
    if (destination == self_ip):
        continue
    print("\tAttempting to ping \"" + destination + "\"")
    res = subprocess.Popen(["ping", "-c 2", "-W 6", destination], stdout=subprocess.PIPE)
    res.communicate()
    if (res.returncode != 0):
        print("\t\tFAILED")
        sys.exit(1)
    else:
        print("\t\tSUCCESS")

print("HOSTNAME TEST-------------------------------------------------")
valid_hostnames = ["gw", "server", "client-1", "client-2"]
hostname_call = subprocess.Popen(["hostname"], stdout=subprocess.PIPE)
self_hostname = hostname_call.communicate()[0].strip().decode("utf-8")

if (hostname_call.returncode != 0):
    print("Unable to get own hostname, exiting")
    sys.exit(1)

print("\tChecking own hostname")
if (self_hostname not in valid_hostnames):
    print("\t\tFAILED, own hostname is \"" + self_hostname + "\"")
    sys.exit(1)
else:
    print("\t\tSUCCESS")

if (self_hostname != "gw"):
    sys.exit(0)

print("ROUTING TEST\"----------------------------------------------------")
routing_call = subprocess.Popen(["nc", "-z", "localhost", "2602"], stdout=subprocess.PIPE)
print("\tChecking if routing daemon is up")
routing_call.communicate()
if (routing_call.returncode != 0):
    print("\t\tFAILED")
    sys.exit(1)
else:
    print("\t\tSUCCESS")
