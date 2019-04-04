# Release Note

	AutoDCR - automatization device configurations and reporting

Version: 0.3.4

## Introduction:

	The document communicates the major new features and changes in this release of the AutoDCR. 
	It also documents known problems and workarounds.

## Compatible Products:

	This product has been tested on the following platforms or with the following products:
		* Python 2.7.5 and 3.6
		* Cisco IOS, Linux OS

## New Features:

	* 1 Request user for search value.
	* 2 Set timeout for execution commands.

	  Use:
	  
		## 1 Request user for search value.

		You can use real time request user for value that will be used in next command in 'search' part

		### Use

		For use this feature you need:
		1 prepare command that will be request user
		2 prepare command with variable name {usr_req} in setion 'search'
	
		### Example
```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker
Request search value;Enter search value:;usr_req;;;;
l2vpn status;Sho l2vpn atom vc;;1;(?P<If>\S+)\s+(?P<PeerID>\S+)\s+(?P<vcid>\d+)\s+\S+\s+(?P<Name>{usr_req})\s+DOWN;complex; Err !,Ok
```
		## 2 Set timeout for execution commands.
		
		### Use

		For use this feature you need:
			1 set in section 'command' keyword - 'timeout'
			2 set in section 'delay_factor' timeout  in second

		### Example
```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker
Waite5s;timeout;;5;;;
```
[For details see](../docs/commands.md)
	
## Limitations:
	
	* Feature tested only with Cisco IOS
	
----

[Home](../README.md)