# Utils

Scripts for helps prepering commands list. 

## commands_gen.py

Script prepare list of commands for executing on each node in list.

### General logic:

Script replace all variables {num} in config_template from arguments of command line 'value' and create command.csv file for script 
batch_cmd_exec  {num}: num equals number in the arguments line (starting from 0)

### Limitations:

Only with Cisco IOS.

### Using:
 
 1. Check installation of Python (tested on Python 2.7.5 )
 2. Copy data in config_template file (same directory)
 3. Execute ./commands_gen.py
 
 ```
	usage: commands_gen.py [-h] [-logic logic] [-var value [value ...]]
                       [-prncnf print cnf]
					   
	optional arguments:
	  -h, --help            show this help message and exit
	  -logic logic          Set logic of executing command: 
				  sh_cmd      - show command;
				  cnf_cmd     - line by line (with possibility of check on error and stop execution script; 
				  cnf_cmd_lst - by command list (set of command) (default = cnf_cmd_lst))
	  -var value [value ...]Set of values of variables than will be replaced inconfig_parrent
	  -prncnf print cnf     Print nativ configuration whith replaced all variables
```

#### Example:

*config_template:*

```
	interface GigabitEthernet0/{0}
	description {1}
	exit
```	

execute script:

```
./commands_gen.py 2 Test_script
```

*result of parcing template:*

```
	interface GigabitEthernet0/2
	description Test_script
	exit		  
```

*result file commands.csv:*

```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker;expect
CnfCmdList;interface GigabitEthernet0/2,description Test_script,exit;conf_set;1;prompt;count;;
WriteMem;write memory;general;1;OK;simple;Ok,Attention!;
```

----

## test_search_parrent.py

Script helps test regex_parrent that will be used for parameter *search* in command file

### Using:

1. Copy output data of executing command in test_output file (same directory)

2. Set regex parrent for testing in body of script, example:

	regex_parrent = '(Model number)(?:\s+:)( \S+)(?:\n)(System serial number)(?:\s+:) (\S+)'
	
3. Set search type: simple|complex|count, example:

	search_type = 'simple'

4. Execute script:

	./test_search_parrent.py

----

[Home](../README.md)