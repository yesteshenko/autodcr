# Release Note

	AutoDCR - automatization device configurations and reporting

Version: 0.3.1

## Introduction:

	The document communicates the major new features and changes in this release of the AutoDCR. 
	It also documents known problems and workarounds.

## Compatible Products:

	This product has been tested on the following platforms or with the following products:
		* Python 2.7.5 and 3.6
		* Cisco IOS, Linux OS

## New Features:

	* 1 SSH connections through device to another device.
	* 2 Possibility set directly nodename that need to use for get set of variables from variables tablefor dynamically configuration templates in commands file

	  Use:
	  
		## 1 SSH connections

		### Use

		For use this feature you need to set RegExp string to section 'expect' for search prompt string.	
	
		### Example
```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker;expect
Connect;ssh 192.168.1.1;conf_cmd;1;request;simple;Ok,Error!;Password:
EntPassw;Psw;;1;.*#$;simple;Ok,Error!;.*#$
```

		## 2 Choice set of variables for replace in template from variables table by setting directly nodename.

		This feature use for example if you connect to another device.

		### Use
		
		For use this feature you need to set 'Nodemane' after 'template_filename' and 'vartable_filename' in section 'command' using delimiter - ','
		
		### Example

```
Config;template_filename.tpl,var_filename_.csv,Node_L;conf_tpl;1;prompt;;
```


[For details see](../docs/configuration_template.md)
	
## Limitations:
	
	* Feature tested only with Cisco IOS
	
----

[Home](../README.md)