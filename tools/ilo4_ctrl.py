#!/usr/bin/env python
##
## Out of Ban Management script for HP OSIC bare metal
##
## https://github.com/seveas/python-hpilo
##
__author__ = 'Dennis DeMarco'

import os, argparse, warnings, sys, subprocess

base_dir = os.path.abspath('..').split('osic-baremetal-tools')[0]
lib_path = os.path.abspath(os.path.join(base_dir, 'osic-baremetal-tools/lib'))
sys.path.append(lib_path)


from osic import cluster

# HP Ilo loves to toss warnings
warnings.filterwarnings("ignore")


def args():
    """Setup argument Parsing."""
    parser = argparse.ArgumentParser(
        usage='%(prog)s',
        description='OSIC ILO4 Control',
        epilog='Verson 1.0')

    parser.add_argument(
        '--powerup',
        help='Power up nodes if OFF',
        required=False,
        default=False,
        action='store_true'

    )

    parser.add_argument(
        '--powerdown',
        help='Power down nodes if ON',
        required=False,
        default=False,
        action='store_true'

    )

    parser.add_argument(
        '-r',
        '--powercycle',
        help='PowerCycle nodes / reboot',
        required=False,
        default=False,
        action='store_true'

    )

    parser.add_argument(
        '-x',
        '--exclude',
        help='Exclude devices',
        required=False,
        nargs="+",
        default=[]

    )

    parser.add_argument(
        '-s',
        '--powerstate',
        help='Reports the powerstate of a device',
        required=False,
        default=False,
        action='store_true'

    )

    parser.add_argument(
        '-i',
        '--include',
        help='Include only these devices, nothing else',
        required=False,
        nargs="+",
        default=[]

    )


    parser.add_argument(
        '-u',
        '--user',
        help='Username to use to connect ILO4',
        required=True
    )

    parser.add_argument(
        '-p',
        '--password',
        help='Password to use to connect to ILO4',
        required=True
    )

    parser.add_argument(
        '--ping',
        help='Ping the OOB port',
        required=False,
        action='store_true'
    )


    parser.add_argument(
        '-n',
        '--netboot',
        help='Set netboot on devices',
        required=False,
        default=False,
        action='store_true'
    )

    parser.add_argument(
        '-b',
        '--bootorder',
        help='Find the Boot order of the devices',
        required=False,
        default=False,
        action='store_true'
    )


    parser.add_argument(
        '--netmacs',
        help='Use ILO to fetch network MAC addresses',
        required=False,
        default=False,
        action='store_true'
    )

    parser.add_argument(
        '-f',
        '--file',
        help='config file. Default: [ %(default)s ]',
        required=False,
        default='cloud-9'
    )

    parser.add_argument(
        '-c',
        '--config-dir',
        help='Configuration Directory: Default: [ %(default)s ]',
        required=False,
        default='../configs'
    )
    return vars(parser.parse_args())


def ping(host):
    """
    Returns True if host responds to a ping request
    """
    with open(os.devnull, 'wb') as devnull:
       try:
          return subprocess.check_call(['fping','-t 100', host], stdout=devnull, stderr=subprocess.STDOUT) ==0
       except:
           return False

def main():

   user_args = args()
   username = user_args['user']
   password = user_args['password']
   config_dir = user_args['config_dir']
   filename = user_args['file']


   cloud = cluster(config_dir + "/yml/" + filename + ".yml")

   for node in cloud:


      if str(node.get('device')) in user_args['exclude']:
           continue

      if user_args['include']:
         if str(node.get('device')) not in user_args['include']:
           continue

      if user_args['netmacs']:
          print "Device #: %s - Net MACS : %s" % (node.get('device'), node.get_oob_netmacs(username, password))

      if user_args['ping']:

          if not (ping(node.get('oob_ip'))):
              print "%s - OOB does not respond to ping." % node.get('name')
          else:
              print "%s - OOB OK." % node.get('name')

      if user_args['bootorder']:
          order = node.oob_getboot(username, password)
          print "Device #: %s - %s" % (node.get('device'),order)

      if user_args['netboot']:
          print "NetBoot on Device #: %s - %s" % (node.get('device'), node.oob_boot_override_pxe(username,password))

      if user_args['powerstate']:
        try:
            powerstate = node.get_oob_powerstate(username,password)
        except:
            powerstate="ERROR: Timeout"
        print "Device # %s is : %s " % (node.get('device'), powerstate)

      if user_args['powercycle']:
          print "Device # %s is power-cycled: %s " % (node.get('device'), node.oob_powercycle(username,password) )

      if user_args['powerup']:
          print "Powering up device #: %s : %s" % (node.get('device'),node.oob_powerup(username,password))

      if user_args['powerdown']:
          try:
             powerstate = node.oob_powerdown(username,password)
          except:
             powerstate = "ERROR: Timeout"
          print "Powering down device #: %s : %s" % (node.get('device'),powerstate)

if __name__ == "__main__":
    main()