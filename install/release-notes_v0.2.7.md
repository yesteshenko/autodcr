# Release Note

	AutoDCR - automatization device configurations and reporting

Version: 0.2.7

## Introduction:

	The document communicates the major new features and changes in this release of the AutoDCR. 
	It also documents known problems and workarounds.

## Compatible Products:

	This product has been tested on the following platforms or with the following products:
		* Python 2.7.5 and 3.6
		* Cisco IOS, Linux OS

## New Features:

	* Possibility use configuration templates for apply in device.
	  
	  Use:
	  
		Use argument list of CLI


		* Create configurations template and put in subdirectory' data'.
		* Set file name to parameter 'conf_template' in autodcr.conf or CLI, for example conf_template = conf_template_test.tpl
		* If need, you can use variables in configurations template (not necessary).


[For details see](../docs/configuration_template.md)
	
## Limitations:
	
	* Feature tested only with Cisco IOS
	
----

[Home](../README.md)