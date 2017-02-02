# /usr/bin/env python

__author__ = 'Dennis De Marco'

import yaml, requests, warnings
import iptools as ipmgr
from netaddr import *


### The library currently requires python-hpilo. I'd like to drop this library
### In favor for Redfish / REST API.

try:
    import hpilo
except ImportError:
    pass

## Turn off Warnings, Libraries complain with self signed certificates on the ILO4 interfaces

requests.packages.urllib3.disable_warnings()
warnings.filterwarnings("ignore")

class node:
    def __init__(self, id, yml_data):
        self.id = id
        self.__dict__.update(yml_data)
        self.netmac = {}

    def __str__(self):
        return str(self.id)

    def get(self, key=None):
        if key == None:
            return self.__dict__.keys()
        else:
            return self.__dict__[key]

    def get_oob_netmacs(self, oob_username=None, oob_password=None):
        ilo = hpilo.Ilo(self.get('oob_ip'), oob_username, oob_password)
        data = ilo.get_host_data()

        for item in data:
            if 'MAC' in item:
                self.netmac[item['Port']]=item['MAC']
        return self.netmac

    def get_oob_powerstate(self, oob_username=None, oob_password=None):
        ilo = hpilo.Ilo(self.get('oob_ip'), oob_username, oob_password)
        oob_return = ilo.get_host_power_status()

        # standardize the response

        if "ON" in oob_return:
            oob_return = "ON"

        if "OFF" in oob_return:
            oob_return = "OFF"

        return oob_return

    def oob_powercycle(self, oob_username=None, oob_password=None):
        oob_return = "Unknown power status"
        ilo = hpilo.Ilo(self.get('oob_ip'), oob_username, oob_password)
        oob_return = ilo.reset_server()

        oob_return = "OK"
        return oob_return

    def oob_powerdown(self, oob_username=None, oob_password=None):
        oob_return = "Unknown"
        ilo = hpilo.Ilo(self.get('oob_ip'), oob_username, oob_password)
        oob_return = ilo.set_host_power(host_power=False)

        if oob_return == None:
            oob_return = "OK"

        return oob_return

    def oob_powerup(self, oob_username=None, oob_password=None):

        oob_return = "Unknown"
        ilo = hpilo.Ilo(self.get('oob_ip'), oob_username, oob_password)

        oob_return = ilo.set_host_power(host_power=True)
        oob_return = "OK"

        return oob_return

    def set_ip(self,ipmgmr,ip=None):
        if ip is None:
            self.ip=ipmgmr.get('PXE')
        else:
            self.ip=ip

    def set_gateway(self,gw):
        self.gateway=gw

    def set_netmask(self,netmask):
        self.netmask=netmask



## Not sure if useful, but added

    def oob_getboot(self, oob_username=None, oob_password=None):
        oob_return = "Unknown"
        ilo = hpilo.Ilo(self.get('oob_ip'), oob_username, oob_password)
        oob_return = ilo.get_persistent_boot()

        return oob_return

    def oob_boot_override_pxe(self, oob_username=None, oob_password=None):
        url = "https://%s/rest/v1/Systems/1" % self.get('oob_ip')
        auth = (oob_username, oob_password)
        headers = {"Content-type": "application/json"}

        data = {
            "Boot": {
                "BootSourceOverrideTarget": "Pxe",
                "BootSourceOverrideEnabled": "Continuous"
            }
        }
        try:
            r = requests.patch(url, json=data, headers=headers, verify=False, auth=auth)
        except:
            return "FAIL"
        if r.status_code == requests.codes.ok:
            return "PASS"
        else:
            return "FAIL"


class cluster:
    def __init__(self, filename):
        with open(filename) as data_file:
            cluster_data = yaml.load(data_file)

        self.cluster_name = cluster_data.keys()[0]
        self.__dict__.update(**cluster_data[self.cluster_name])

        # Let's convert the yaml into our objects

        self.node_dict = {}
        for item in self.nodes:
            self.node_dict[item] = node(item, self.nodes[item])

        # Drop the nodes key, as we now objectify the data
        self.__dict__.pop('nodes', None)

    def __str__(self):
        return self.cluster_name

    def __iter__(self):
        return self.node_dict.itervalues()

    def __len__(self):
        return len(self.node_dict)

    def get_node(self, node_id):
        return self.node_dict[node_id]

    def get(self, key=None):
        if key == None:
            return self.__dict__.keys()
        else:
            return self.__dict__[key]

    def get_deploy(self,key=None):
        if key == None:
            return self.deploy_host.keys()
        else:
            return self.deploy_host[key]

    def dump_config(self,directory):
        pass

    def dump_cobbler(self,directory):
        pass

    def generate_ips(self,network,gateway):

        ip = IPNetwork(network)
        _tmp = []

        ## First 20 are used in each lab for network gear
        self.ip_manager = ipmgr.IPManager(queues={'PXE':network}, used_ips=[str(ip.ip)[0:-1]+ str(i) for i in range(1,21)])

        # Let's get some IP addresses for the deployment node configuration

        self.deploy_host['gateway'] = gateway

        self.deploy_host['br-pxe'] = self.ip_manager.get('PXE')
        self.deploy_host['container_ip'] = self.ip_manager.get('PXE')
        self.deploy_host['netmask'] = ip.netmask

        # Now dish out ip addresses to the nodes

        for node in self.node_dict:
            self.node_dict[node].set_ip(self.ip_manager)
            self.node_dict[node].set_gateway(gateway)
            self.node_dict[node].set_netmask(ip.netmask)

            # Build a list of IP's assigned for dhcp_ranges

            _tmp.append(self.node_dict[node].get('ip'))

        self.dhcp_range =ipmgr.merge_ip_list(_tmp)

    def return_id_devices(self):
        tmp = []
        for node in self:
            tmp.append(node.get('device'))
        return tmp

if __name__ == '__main__':
    pass