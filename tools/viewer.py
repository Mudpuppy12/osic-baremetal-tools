#!/usr/bin/env python
#
## Basic script to display

import os,sys

base_dir = os.path.abspath('..').split('osic-baremetal-tools')[0]
lib_path = os.path.abspath(os.path.join(base_dir, 'osic-baremetal-tools/lib'))
sys.path.append(lib_path)


from osic import cluster
from pprint import pprint

config_dir = "../configs"


cloud = cluster(config_dir + "/templates/cloud9.dyml")


print "The cloud name is %s: " % (cloud)
print "It has %s nodes." % (len(cloud))

print "The node names are:"

for node in cloud:
  print node.get("name")
