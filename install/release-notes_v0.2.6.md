# Release Note

	AutoDCR - automatization device configurations and reporting

Version: 0.2.6

## Introduction:

	The document communicates the major new features and changes in this release of the AutoDCR. 
	It also documents known problems and workarounds.

## Compatible Products:

	This product has been tested on the following platforms or with the following products:
		* Python 2.7.5 and 3.6
		* Cisco IOS, Linux OS

## New Features:

	* Possibility to set regular expression pattern to use for determining end of output in reading channel process.
	  
	  Use:
		Set regular expression pattern to parameter 'expect' for command in commands file, for example: expect = .*#$
			
			Example commands file:
			
			cmdname;command;cmd_type;delay_factor;search;search_type;result_marker;expect
			Get versions;sh ver;;;Cisco IOS Software, (?P<version>\w+);simple;;.*#$

## Limitations:
	
	* Feature tested only with Cisco IOS
	
----

[Home](../README.md)