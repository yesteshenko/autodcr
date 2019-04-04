# Release Note

	AutoDCR - automatization device configurations and reporting

Version: 0.3.3

## Introduction:

	The document communicates the major new features and changes in this release of the AutoDCR. 
	It also documents known problems and workarounds.

## Compatible Products:

	This product has been tested on the following platforms or with the following products:
		* Python 2.7.5 and 3.6
		* Cisco IOS, Linux OS

## New Features:

	* 1 Use result value table of previous command report (complex mode) for new command.
	* 2 Add build-in variables

	  Use:
	  
		## 1 Use result value table of previous command report

		You can use report of execution previous command as variable set for use in next command.

		### Use

		For use this feature you need:
		1 prepare command that will be back report in table format (complex mode)
		2 prepare command with variable name same as header of result table (column name)
			Format:
			{$'varname'} - 	will be replaced 'varname' by value of previous command report (complex mode).
		
		Expects table, where 1 row it is 'varname' list, next line it is values list
			
		This command will be executed as many times as many result lines will be.
	
		### Example
```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker
l2vpn status;Sho l2vpn atom vc;;1;(?P<If>\S+)\s+(?P<PeerID>\S+)\s+(?P<vcid>\d+)\s+\S+\s+(?P<Name>l3vpn\S+)\s+DOWN;complex; Err !,Ok
l2vpn status detail;Sho l2vpn atom vc vcid {$vcid} detail;;1;(?P<Line>.*)(?P<Status>DOWN);complex; Err !,Ok
```
		## 2 Build-in variables
		
		You can use next variables in section 'command'
			{datetime}	- will be replaced by current date and time
			{date}		- will be replaced by current date
		You can use next variables in section 'search'
			{nodename} 	- will be replaced by current node name
			{nodeip} 	- will be replaced by current node ip
			{datetime}	- will be replaced by current date and time
			{date}		- will be replaced by current date

[For details see](../docs/commands.md)
	
## Limitations:
	
	* Feature tested only with Cisco IOS
	
----

[Home](../README.md)