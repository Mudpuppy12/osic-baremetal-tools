#!/usr/bin/env python
#
## This script will take a template file and generate a detailed
## configuration for the lab environment.

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
        '-u',
        '--user',
        help='Username to use to connect ILO4',
        required=False,
        default='root'
    )

    parser.add_argument(
        '-p',
        '--password',
        help='Password to use to connect to ILO4',
        required=False,
        default=''
    )


    parser.add_argument(
        '-c',
        '--config-dir',
        help='Configuration Directory: Default: [ %(default)s ]',
        required=False,
        default='../configs'
    )

    parser.add_argument(
        '-n',
        '--network',
        help='PXE network to configure: Default: [ %(default)s ]',
        required=False,
        default='172.23.0.0/22'
    )

    parser.add_argument(
        '-gw',
        '--gateway',
        help='PXE network Gateway to configure: Default: [ %(default)s ]',
        required=False,
        default='172.23.0.1'
    )

    return vars(parser.parse_args())

def main():

   user_args = args()

   username = user_args['user']
   password = user_args['password']
   config_dir = user_args['config_dir']
   network = user_args['network']
   filename = user_args['file']
   gateway = user_args['gateway']

   cloud = cluster(config_dir + "/templates/" + filename + ".tmpl")
   cloud.generate_ips(network,gateway)
   cloud.dump_config()

if __name__ == "__main__":
    main()