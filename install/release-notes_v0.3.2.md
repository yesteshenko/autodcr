# Release Note

	AutoDCR - automatization device configurations and reporting

Version: 0.3.2

## Introduction:

	The document communicates the major new features and changes in this release of the AutoDCR. 
	It also documents known problems and workarounds.

## Compatible Products:

	This product has been tested on the following platforms or with the following products:
		* Python 2.7.5 and 3.6
		* Cisco IOS, Linux OS

## New Features:

	* 1 Set colors scheme
	* 2 Set CLI error keywords

	  Use:
	  
		## 1 colors schemes

		You can set own colors scheme in report.

		### Use

		For this need describe keywords in file [colors.yaml]  in yaml format:
	
		### Example
```
report: 
    OKGREEN:
        1: " Ok "
```

		## 2 CLI error keywords

		You can set CLI errors keywords for check execution of command.

		### Use
		
		For this need write keywords or RegExp in file [cli.err], one by line.	
	
		### Example

```
^Unknown
Invalid input detected
```

[For details see](../docs/userguide.md)
	
## Limitations:
	
	* Feature tested only with Cisco IOS
	
----

[Home](../README.md)