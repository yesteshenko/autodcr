# Release Note

	AutoDCR - automatization device configurations and reporting

Version: 0.3.0

## Introduction:

	The document communicates the major new features and changes in this release of the AutoDCR. 
	It also documents known problems and workarounds.

## Compatible Products:

	This product has been tested on the following platforms or with the following products:
		* Python 2.7.5 and 3.6
		* Cisco IOS, Linux OS

## New Features:

	* RESTful API
	* Because RESTful API not use authorization and use HTTP use this only in secured LAN and for a short time (not as service or daemon)  
	  Use:
	  
		## 1 Use

		You can use Postman or any web browser.	
	
		## Available methods

			## nodes

				This GET method return node[s] parapeters if available. Using for checking correct node configurations.

			### Parameters

				- group	- group name of nodes from yaml data file
				- name	- node name (or all) from yaml data file
				- par	- parameners name for given node from yaml data file

			## cmd

				This GET method executing commands for nodes and returns report.

			### Parameters

				- group				- group name of nodes from yaml data file
				- name				- node name (or all) from yaml data file
				- par				- parameners name for given node from yaml data file
				- commands			- filename of commands list for executing (optional, default value getting from configurations file)
				- conf_template		- configurations template (optional). Can be name of file: filename.tpl or directly commands template
				- conf_template_var - variables for configurations template in json format (optional).
				'						Format:
				'							{ "var_name": "var_value" [, "var_name": "var_value"] }
				'						Buid-in variables:
				'							{nodename}     - will be set current nodename of device,
				'							{nodeip}       - will be set current ip of device

[For details see](../docs/rest_api.md)
	
## Limitations:
	
	* Feature tested only with Cisco IOS
	
----

[Home](../README.md)