# Release Note

	AutoDCR - automatization device configurations and reporting

Version: 0.2.5

## Introduction:

	The document communicates the major new features and changes in this release of the AutoDCR. 
	It also documents known problems and workarounds.

## Compatible Products:

	This product has been tested on the following platforms or with the following products:
		* Python 2.7.5 and 3.6
		* Cisco IOS, Linux OS

## New Features:

	* Added possibility of controll maximum number of parallel processes when using multiprocessing mode
	  
	  Use:
		1 Set type of logic of processing nodes to parameter 'multiprocessing_exec' in autodcr.conf, for example: multiprocessing_exec = True
				multiprocessing 		= True, 
				singlrocessing (exec in queue) 	= False
		2 Set maximum number of parallel processes to parameter 'max_process' in autodcr.conf, for example: max_process = 100 (Not recomended set huge value)


## Limitations:
	
	* Feature tested only with Cisco IOS
	
----

[Home](../README.md)