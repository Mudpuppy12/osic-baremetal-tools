#!/usr/bin/env python
#

import os,sys, argparse

base_dir = os.path.abspath('..').split('osic-baremetal-tools')[0]
lib_path = os.path.abspath(os.path.join(base_dir, 'osic-baremetal-tools/lib'))
sys.path.append(lib_path)


from osic import cluster
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('../configs/templates'))
template = env.get_template('cobbler_system.j2')


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
        '-i',
        '--interface',
        help='interface to boot on. Default: [ %(default)s ]',
        required=False,
        default= 'p1p1'
    )

    parser.add_argument(
        '-c',
        '--config-dir',
        help='Configuration Directory: Default: [ %(default)s ]',
        required=False,
        default='../configs'
    )

    parser.add_argument(
        '-p',
        '--profile',
        help='Cobbler profile to use: Default: [ %(default)s ]',
        required=False,
        default='ubuntu-14.04.3-server-unattended-osic-generic'
    )

    parser.add_argument(
        '--dns',
        help='DNS to use: Default: [ %(default)s ]',
        required=False,
        default='8.8.8.8'
    )

    return vars(parser.parse_args())

def return_mac(interface,netmacs):
   # This is a guess for now, only data I had was cloud9, which the first netmac was p1p1 because
   # on board was disabled in BIOS

   # A Lenth of 5 means onboard is disabled except for ILO

   if len(netmacs) ==5:
       if interface in 'p1p1:':
           return netmacs[1]
   else: # First 4 on board, 5 ILO, this must be p1p1?
       if interface in 'p1p1':
           return netmacs[6]

   return "AA:BB:CC:DD:EE:FF"

def main():

   user_args = args()

   config_dir = user_args['config_dir']
   filename = user_args['file']


   cloud = cluster(config_dir + "/yml/" + filename + ".yml")

   for node in cloud:
       hostname = node.get('name')
       ip = node.get('ip')
       netmask = node.get('netmask')
       gateway = node.get('gateway')

       interface = user_args['interface']
       netmacs = node.get('netmac')
       profile = user_args['profile']
       dns = user_args['dns']

       mac = return_mac(interface,netmacs)

       output = template.render(hostname=hostname, mac=mac, ip=ip, netmask=netmask, gateway=gateway, dns=dns, interface=interface, profile=profile)
       print output + "\n"
if __name__ == "__main__":
    main()