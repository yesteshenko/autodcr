# Changelog
    
    All notable changes to this project will be documented in this file.

## [0.3.5](release-notes_v0.3.5.md)

    ### Added
	- Possibility realtime request user for value that will be used in next command in 'command' part based on report previous comman
    ### Fix
	- Fix bags
		
## [0.3.4](release-notes_v0.3.4.md)

    ### Added
	- Possibility realtime request user for value that will be used in next command in 'search' part
	- Possibility set timeout for execution commands.
    ### Fix
	- Fix bags
	
## [0.3.3](release-notes_v0.3.3.md) 

    ### Added
	- Possibility using result value table of previous command report (complex mode) for new command.
	- build-in variables for replace in 'command' and 'search' sections in commands file.
    ### Fix
	- Fix bags
	
## [0.3.2](release-notes_v0.3.2.md) 

    ### Added
	- Possibility of setting own colors scheme in report.
	- Possibility of setting CLI errors keywords for check execution of command.
    ### Fix
	- Fix bags
		
## [0.3.1](release-notes_v0.3.1.md) 

    ### Added
        - Possibility of SSH connections through device to another device
	- Possibility set directly nodename that need to use for get set of variables from variables table for dynamically configuration templates in commands file

## [0.3.0](release-notes_v0.3.0.md) 

    ### Added
        - RESTful API
	
## [0.2.9](release-notes_v0.2.9.md) 

    ### Added
        - Possibility use dynamically configuration templates in commands file for apply in device can be used variables table 
		
## [0.2.8](release-notes_v0.2.8.md) 

    ### Added
        - Possibility use dynamically configuration templates in commands file for apply in device
    ### Fix
        - Fix bags if using Python v3

## [0.2.7](release-notes_v0.2.7.md) 

    ### Added
        - Possibility use configuration templates for apply in device
    ### Fix
        - Fix bags in report using TextFSM
        - Fix error when executing command on Cisco XR

## [0.2.6](release-notes_v0.2.6.md) 

    ### Added
        - Possibility to set regular expression pattern to use for determining end of output in reading channel process.		
    
## [0.2.5](release-notes_v0.2.5.md) 

    ### Added
        - Possibility  of controll maximum number of parallel processes when using multiprocessing mode
    
## [0.2.4](release-notes_v0.2.4.md) 

    ### Added
        - Possibility use YAML format in nodes configuration file
    ### Fix
        - Error when use wrong separator in incoming data command file
    
## [0.2.3](release-notes_v0.2.3.md) 

    ### Added
        - Possibility use result report of previous command for send to shell OS command
    
## [0.2.2](release-notes_v0.2.2.md) 

    ### Added
        - Possibility parse output of command execution by TextFSM module and templates in subdir TextFSMtemplates

    ### Fix
        - Fix bags in report

## [0.2.1](release-notes_v0.2.1.md) 

    ### Added
        - Export result of command execution to excel or word

    ### Fix
        - Fix bags in report

## [0.1.9] 

    ### Added
        - Possibility print only last found result
        - Documentations

    ### Fix
        - Fix bags in report
        
## [0.1.8] 

    ### Added
        - Key word in report (result_marker)

    ### Fix
        - Fix bags in report
        
## [0.1.7] 

    ### Added
        - Possibility using result value of previous command in variable {} in current command

    ### Fix
        - Fix bags in report
        
## [0.1.6] 

    ### Added
        - Command line for set parameters

    ### Fix
        - Fix bags in report        

## [0.1.5] 

    ### Added
        - Tools for generations command.csv from template

    ### Fix
        - Fix bags in report
        
## [0.1.4] 

    ### Added
        - Tools for testing regex parent

    ### Fix
        - Fix bags in report
        
## [0.1.3] 

    ### Added
        - Using group name in regex parent for header in summary report table 

    ### Fix
        - Fix bags in report
        
## [0.1.2] 

    ### Added
        - Possibility set delay factor for command execution

    ### Fix
        - Fix bags in report
        
## [0.1.1] 

    ### Added
        - Executing command in config mode: type of command

    ### Fix
        - Fix bags in report
        

## [0.0.9] 

    ### Added
        - Compatibility with  python 3

    ### Fix
        - Fix bags in report

## [0.0.8] 

    ### Added
        - Sorting mode by commands or nodes

    ### Fix
        - Fix bags in report
        
## [0.0.7] 

    ### Added
        - Advanced logic for search in output of command execution (search_type)

    ### Fix
        - Fix bags in report
        
## [0.0.6] 

    ### Added
        - Checking executing commands for search value

    ### Fix
        - Fix bags in report
        
## [0.0.5] 

    ### Added
        - Checking executing commands for error

    ### Fix
        - Fix bags in report
        
## [0.0.4] 

    ### Added
        - Multiprocessing mode

    ### Fix
        - Fix bags in report
        
## [0.0.3] 

    ### Added
        - Create summary result of command execution    

## [0.0.2] 

    ### Added
        - Export result of command execution to file
        
## [0.0.1] 

    ### Added
        - Basic command execution in batch mode

----
    
[Home](../README.md)