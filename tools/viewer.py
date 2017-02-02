#!/usr/bin/env python
#

import os,sys, argparse

base_dir = os.path.abspath('..').split('osic-baremetal-tools')[0]
lib_path = os.path.abspath(os.path.join(base_dir, 'osic-baremetal-tools/lib'))
sys.path.append(lib_path)


from osic import cluster

def args():
    """Setup argument Parsing."""
    parser = argparse.ArgumentParser(
        usage='%(prog)s',
        description='OSIC bare metal config generator',
        epilog='Version 1.0"'
    )

    parser.add_argument(
        '-f',
        '--file',
        help='config file. Default: [ %(default)s ]',
        required=False,
        default= 'cloud-9'
    )


    parser.add_argument(
        '-c',
        '--config-dir',
        help='Configuration Directory',
        required=False,
        default='../configs'
    )

    return vars(parser.parse_args())

def main():

   user_args = args()

   config_dir = user_args['config_dir']
   filename = user_args['file']


   cloud = cluster(config_dir + "/yml/" + filename + ".yml")

   print "The cloud name is: %s" % cloud
   print "The cloud has %s nodes" % len(cloud)

   print "The deployment node is: %s" % cloud.get_deploy('name')
   print "This is not included in the node count.\n"

   print "The node names are:"

   for node in cloud:
     print node.get('name')


if __name__ == "__main__":
    main()