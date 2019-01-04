# Nodes

## Introduction:

  The document describe rules and helps to prepare list of nodes with connections parameters for executing commands.
It also documents examples.

## csv file format:

First line contains variables name what will be used for connections;
next lines contains value of each node;
parameters separator is comma - ';'.

### Example:

```
nodename;ip;username;password;secret;device_type
node1;192.168.1.1;cisco;cisco;cisco;cisco_ios
node2;192.168.1.2;cisco;cisco;cisco;cisco_ios
```    
## yaml file format:

Create group of device that include device hostname and ip
Create authoryzation parameters for device

### Example:

```
cisco_param:
  username:
    cisco
  password:
    cisco
  secret:
    ''
  device_type:
    cisco_ios

cisco:
  node1:
    192.168.1.1
  node2:
    192.168.1.2
```

## Parameters descriptions:

	  nodename     - first variable used for name of generated output report file for each node

	  ip           - IP address node

	  username     - username

	  password     - password

	  secret       - password for enable (for cisco)

	  device_type  - type of device pyton lib: Netmiko (https://github.com/ktbyers/netmiko) 
				Supports: Regularly tested
					a10
					accedian
					alcatel_aos
					alcatel_sros
					apresia_aeos
					arista_eos
					aruba_os
					avaya_ers
					avaya_vsp
					brocade_fastiron
					brocade_netiron
					brocade_nos
					brocade_vdx
					brocade_vyos
					calix_b6
					checkpoint_gaia
					ciena_saos
					cisco_asa
					cisco_ios
					cisco_nxos
					cisco_s300
					cisco_tp
					cisco_wlc
					cisco_xe
					cisco_xr
					coriant
					dell_dnos9
					dell_force10
					dell_isilon
					dell_os10
					dell_os6
					dell_os9
					dell_powerconnect
					eltex
					enterasys
					extreme
					extreme_ers
					extreme_exos
					extreme_netiron
					extreme_nos
					extreme_slx
					extreme_vdx
					extreme_vsp
					extreme_wing
					f5_linux
					f5_ltm
					f5_tmsh
					fortinet
					generic_termserver
					hp_comware
					hp_procurve
					huawei
					huawei_vrpv8
					ipinfusion_ocnos
					juniper
					juniper_junos
					linux
					mellanox
					mrv_optiswitch
					netapp_cdot
					netscaler
					ovs_linux
					paloalto_panos
					pluribus
					quanta_mesh
					rad_etx
					ruckus_fastiron
					ubiquiti_edge
					ubiquiti_edgeswitch
					vyatta_vyos
					vyos
					and other Limited testing, Experimental ....
					(and cisco_ios_telnet)
----

[Home](../README.md)