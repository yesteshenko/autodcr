# Release Note

	AutoDCR - automatization device configurations and reporting

Version: 0.2.4

## Introduction:

	The document communicates the major new features and changes in this release of the AutoDCR. 
	It also documents known problems and workarounds.

## Compatible Products:

	This product has been tested on the following platforms or with the following products:
		* Python 2.7.5 and 3.6
		* Cisco IOS, Linux OS

## New Features:

	* Added possibility use YAML format in nodes configuration file
	  
	  Use:
		1 Create node configurations and put in subdirectory data. 
			yaml file format:
				Create group of device that include device hostname and ip
				Create authoryzation parameters for device
		2 Set file name to parameter 'nodes' in autodcr.conf or CLI, for example: nodes  = nodes.yaml
		3 Set type of config file for import nodes: for CSV format - csv, for YAML format - yaml to parameter 'nodes_type' in autodcr.conf or CLI, for example: nodes_type = yaml
		4 Set of values of nodes from yaml data file for using to parameter 'nodes_set' in autodcr.conf or CLI, for example: nodes_set  = cisco node1 cisco_param 
			Arguments: 
				1st:  	group, 
				2nd: 	node_name or all, 
				3rd: 	parameners

	  Example:
		configurations nodes:
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
		CLI:
		```
		./autodcr.py -commands commands_bad.csv -nodes_set cisco node1 cisco_param
		./autodcr.py -commands commands_bad.csv -nodes_set cisco all cisco_param
		```

## Limitations:
	
	* Feature tested only with Cisco IOS
	
----

[Home](../README.md)