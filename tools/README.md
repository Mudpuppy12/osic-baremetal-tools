#Tooling
This directory contains all the tooling you need make your life easier
managing the bare hardware labs for OSIC

## generate_config.py
This helper script will take a template and populated it with
the network information for your lab.

<pre>
usage: generate_config.py

OSIC bare metal config generator

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  config file. Default: [ cloud-9 ]
  -c CONFIG_DIR, --config-dir CONFIG_DIR
                        Configuration Directory
  -n NETWORK, --network NETWORK
                        PXE network to configure
  -gw GATEWAY, --gateway GATEWAY
                        PXE network Gateway to configure

Version 1.0"
</pre>

##Usage example

<pre>
# ./generate_config.py -n 172.23.0.0/22 -gw 172.23.0.1 -f cloud-9
</pre>

This will take the template for cloud 9, using the ip addresses you provided
to assign ip addresses to the nodes. It will then dump the assignments into
the config directory as <cloud_name>.yml.

This is useful to generate ip address for cobbler for your nodes.

You can always edit the templates to get what you want on what nodes.


## viewer.py
This is a simple script to display things about your cluster that
you generated from the config. Used to display some of the functionality
of the libraries

<pre>
usage: viewer.py

OSIC bare metal viewer

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  config file. Default: [ cloud-9 ]
  -c CONFIG_DIR, --config-dir CONFIG_DIR
                        Configuration Directory: Default: [ ../configs ]

Version 1.0
</pre>

## generate_cobbler.py
This script was created to improve generating the cobbler system
initalization.

https://github.com/rsoprivatecloud/osic-bare-metal-deployment-process

<pre>
usage: generate_cobbler.py

OSIC bare metal config generator

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  config file. Default: [ cloud-9 ]
  -i INTERFACE, --interface INTERFACE
                        interface to boot on. Default: [ p1p1 ]
  -c CONFIG_DIR, --config-dir CONFIG_DIR
                        Configuration Directory: Default: [ ../configs ]
  -p PROFILE, --profile PROFILE
                        Cobbler profile to use: Default: [ ubuntu-14.04.3
                        -server-unattended-osic-generic ]
  --dns DNS             DNS to use: Default: [ 8.8.8.8 ]

Version 1.0
</pre>

Output as such
<pre>
cobbler system add --name=729446-comp-disk-094.cloud9.osic.rackspace.com --mac=68-05-CA-32-DF-D8 --profile=ubuntu-14.04.3-server-unattended-osic-generic --hostname=729446-comp-disk-094.cloud9.osic.rackspace.com --interface=p1p1 --ip-address=172.23.0.86 --subnet=255.255.252.0 --gateway=172.23.0.1 --name-servers=8.8.8.8 --kopts="interface=p1p1"
</pre>
