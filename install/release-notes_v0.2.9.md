# Release Note

	AutoDCR - automatization device configurations and reporting

Version: 0.2.9

## Introduction:

	The document communicates the major new features and changes in this release of the AutoDCR. 
	It also documents known problems and workarounds.

## Compatible Products:

	This product has been tested on the following platforms or with the following products:
		* Python 2.7.5 and 3.6
		* Cisco IOS, Linux OS

## New Features:

	* Possibility use dynamically configuration templates in commands file for apply in device can be used variables table 
	  
	  Use:
	  
		## 1 Use

		* You can create file with set of variables file for each node and put in subdirectory 'data'.
		* Set in command file in section 'command' - 'filename' and 'vartable_filename' by delimiter ','
		
  ***Example***:


```Config;template_filename.tpl,var_filename_.csv;conf_tpl;1;prompt;;```



[For details see](../docs/configuration_template.md)
	
## Limitations:
	
	* Feature tested only with Cisco IOS
	
----

[Home](../README.md)