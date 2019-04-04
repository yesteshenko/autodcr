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

	* Request user for set of variable.

	  ###Use:
	  

	You can use real time request user for set of value that will be used in next command in 'command' part 


		For use this feature you need:
		1 prepare command that will be back report in table format (complex mode)
		2 prepare command that will be request user for choice variable set based on report from previous command in table format (complex mode)
			For this you need to set in section 'cmd_type' - 'choose_req' and in section 'command' - text for user.
		3 prepare command with variable name same as header of result table (column name)
	
		### Example
```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker
l2vpn status;Sho l2vpn atom vc;;1;(?P<If>\S+)\s+(?P<PeerID>\S+)\s+(?P<vcid>\d+)\s+\S+\s+(?P<Name>l3vpn\S+)\s+DOWN;complex; Err !,Ok
Choose search value;Choose search value:;choose_req;;;;
l2vpn status detail;Sho l2vpn atom vc vcid {vcid} detail;;1;(?P<Line>.*)(?P<Status>DOWN);complex; Err !,Ok
```

[For details see](../docs/commands.md)
	
## Limitations:
	
	* Feature tested only with Cisco IOS
	
----

[Home](../README.md)