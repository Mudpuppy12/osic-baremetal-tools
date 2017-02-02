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

