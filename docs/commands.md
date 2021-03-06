# Commands

## Introduction

The document describe rules and features for command and helps to prepare list of commands for executing on each node in list.
It also documents examples.

----

## csv file format

First line contains variables name what will be used for executing commands;
next lines contains value of each command;
parameters separator is comma - ';'.

----

## Parameters descriptions

	cmdname        - name of command for reporting;

	command        - command than will be send to the node:
			special cmd:
				enter    - send "enter" to the node
				timeout - will be set timeout of execution commands according to 'delay_factor' in second
			special variables:	
				{} in command means use result value of previous command 
				   (expects list of values, for example: 1 or  1,2,3). 
				   This command will be executed as many time as many result value will be.
				<> in command means use result report of previous command for send to shell OS command
				{command} 	- will be replaced by previous command
				{nodename} 	- will be replaced by current node name
				{nodeip} 	- will be replaced by current node ip
				{datetime}	- will be replaced by current date and time
				{date}		- will be replaced by current date
				{$'varname'} - 	will be replaced 'varname' by value of previous command report (complex mode).
					Expects table, where 1 row it is 'varname' list, next line it is values list
					This command will be executed as many times as many result lines will be.
			for conf_tpl mode:
				empty - will be try get configuration template and variables from argument list CLI
				template_filename.tpl[,var_filename_.csv][,nodename] - individual set of templates
					template_filename.tpl	- config template with or without (if not set 'var_filename_.csv') variables 
					var_filename_.csv		- variables for replace in  config template in csv format. 
											 set of variables will be apply according to nodename that currently connected
											 Optional, can be empty
					nodename				- set directly nodename that need to use for get set of variables  from 'var_filename_.csv'
											 Optional, can be empty
					
	cmd_type    - set type of command: (!!!tested only for cisco_ios!!!)
			general (or empty)  - command than not in config mode
			conf_set            - list of command in config mode
								in this mode script will be enter to configutation mode, execute list of command and exit 
			conf_enter          - enter to the config mode
			conf_cmd            - single command in the config mode
			conf_exit           - exit from the config mode
			os_exec             - execute shell OS command
			conf_tpl			- configuration template mode
			usr_req				- request user for value that will be used in next command in 'search' part
			choose_req			- request user for value that will be used in next command in 'command' part based on report previous command
			
	delay_factor    - time for waiting of respond from command execution. Default: 1 - 100 seconds

	search        - string for search in output of command execution. Can be Regex. 
					If use group name in regex parent  ?P<name>, 
					that name will be used for headers in report table.
				special parent: (!!!tested only for cisco_ios!!!)
				prompt        - match current prompt, if no additional output of command execution
				prompt_cnf    - match config prompt, if no additional output of command execution (Regex: '.*\(\S+\)\#$')
				request      - match additional request for command execution (Regex: '.*: $')
				confirm      - match additional confirmation for command execution (Regex: '.* \[.*\]')
				{nodename} 	- will be replaced by current node name
				{nodeip} 	- will be replaced by current node ip
				{datetime}	- will be replaced by current date and time
				{date}		- will be replaced by current date
				{usr_req}	- will be replaced by value from user entered
				
	search_type    - set type of logic parsing result command execution report:
				simple            - output result of search
				complex           - output table of search result (use group in regex parent )
				count (or empty)  - output count of search result (by default)
				'type',last       - output last found result, usable for parsing log. example simple,last or complex,last
				TextFSM           - output table that parsed by TextFSM module and templates in subdir TextFSMtemplates
							(Thanks for templates: https://github.com/networktocode/ntc-templates)
							Docs how to create templates and rules can be found in https://github.com/google/textfsm/wiki/TextFSM
							!!!Templates not verified, if they do not work, try to check syntax by yourself, or contact the author!!!
	
	result_marker        Key word in report. Can be empty
				Format: [parent  is found],[parent  is not found] 
				Example: Ok,Attention!
		
	expect		   - Set regular expression pattern to use for determining end of output in reading channel process. 
				If left blank will default to being based on router prompt (default logic of netmiko module). 
				Change 'expect prompt string' only if default logic netmiko module not work or need different logic of executing commands
				Optional, can be empty

----

                
## Search example:

Example:

```
cmdname;command;delay_factor;search;search_type;result_marker
Get versions;sh ver;1;Cisco IOS Software;simple;
Enter;enter;1;prompt;;
Get voice port;show voice port;1;(ISDN \d\/\d).*\n.*\n (Operation State is \S+)\n (Administrative State is \S+)+;complex;

Commands name: Get versions

------------------------------------------
| nodename                | Result                                                                  |
|:------------------------|:------------------------------------------------------------------------|
| Node_1  | Successful [search: Cisco IOS Software, result: ['Cisco IOS Software']] |
| Node_2  | Successful [search: Cisco IOS Software, result: ['Cisco IOS Software']] |

==========================================

Commands name: Enter

------------------------------------------
| nodename                | Result                               |
|:------------------------|:-------------------------------------|
| Node_1  | Successful [search: prompt, count: 1] |
| Node_2  | Successful [search: prompt, count: 1] |

==========================================

Commands name: Get voice port

------------------------------------------
| nodename                | Result   |
|:------------------------|:---------|
| Node_1   | Successful [complex search, result:
 +----------+----------------------------+----------------------------+
| ISDN 3/0 | Operation State is DORMANT | Administrative State is UP |
+----------+----------------------------+----------------------------+
| ISDN 3/1 | Operation State is DORMANT | Administrative State is UP |
+----------+----------------------------+----------------------------+]          |
| Node_2 | Successful [complex search, result:
 +----------+----------------------------+----------------------------+
| ISDN 3/0 | Operation State is DORMANT | Administrative State is UP |
+----------+----------------------------+----------------------------+
| ISDN 3/1 | Operation State is DORMANT | Administrative State is UP |
+----------+----------------------------+----------------------------+]          |

==========================================

Executing command one by one:

cmdname;command;cmd_type;delay_factor;search;search_type;result_marker
Get versions;sh ver;;1;Cisco IOS Software;simple;
Enter;enter;;1;prompt;;
EntConfT;conf t;conf_enter;1;prompt;;
EntIf0/1;interface GigabitEthernet0/1;conf_cmd;1;prompt;;
AddDesc;description Test_script;conf_cmd;1;prompt;;
ExtIf0/1;exit;conf_cmd;1;prompt;;
ExtConfT;exit;conf_exit;1;prompt;;
WriteM;write memory;;1;OK;simple;

==========================================

   Node name: Node_1

------------------------------------------
| CmdName      | Result                                                                  |
|:-------------|:------------------------------------------------------------------------|
| Get versions | Successful [search: Cisco IOS Software, result: ['Cisco IOS Software']] |
| Enter        | Successful [search: prompt, count: 1]                                    |
| EntConfT     | Successful [search: prompt, count: 1]                                    |
| EntIf0/1     | Successful [search: prompt, count: 1]                                    |
| AddDesc      | Successful [search: prompt, count: 1]                                    |
| ExtIf0/1     | Successful [search: prompt, count: 1]                                    |
| ExtConfT     | Successful [search: prompt, count: 1]                                    |
| WriteM       | Successful [search: OK, result: ['OK']]                                 |

==========================================

Executing list of commands:

cmdname;command;cmd_type;delay_factor;search;search_type;result_marker
Get versions;sh ver;;1;Cisco IOS Software;simple;
AddEntIf0/1Desc;interface GigabitEthernet0/1,description Test_script2,exit;conf_set;1;prompt;;
WriteM;write memory;;1;OK;simple;

Summary report:

==========================================

   Node name: Node_1

------------------------------------------
| CmdName         | Result                                                                  |
|:----------------|:------------------------------------------------------------------------|
| Get versions    | Successful [search: Cisco IOS Software, result: ['Cisco IOS Software']] |
| AddEntIf0/1Desc | Successful [search: prompt, count: 1]                                    |
| WriteM          | Successful [search: OK, result: ['OK']]                                 |

==========================================

Example working with request and confirm dialog

cmdname;command;cmd_type;delay_factor;search;search_type;result_marker
Get versions;sh ver;;1;Cisco IOS Software, (\w+);simple;
Ping;ping vrf l3vpn_mgt;;1;confirm;;
enter;enter;;1;request;;
sendip;172.17.44.3;;1;confirm;;
enter;enter;;1;confirm;;
enter;enter;;1;confirm;;
enter;enter;;1;confirm;;
enter;enter;;1;confirm;;
enter;enter;;1;(?P<ipaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*\n.*\nSuccess rate is (?P<rate>\d{1,3});complex;
```
----

[Home](../README.md)