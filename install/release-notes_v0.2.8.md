# Release Note

	AutoDCR - automatization device configurations and reporting

Version: 0.2.8

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
	  
		## Use command

		! This use case has higher priority than using CLI mode setting configurations template

		* Create configurations template and put in subdirectory 'data'.
		* Set in command file in section 'command' - 'filename' and in section 'cmd_type'  - 'conf_tpl'.

*		**Example***:
```Config;template_filename.tpl;conf_tpl;1;prompt;;```

[For details see](../docs/configuration_template.md)
	
## Limitations:
	
	* Feature tested only with Cisco IOS
	
----

[Home](../README.md)