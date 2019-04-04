Release Note

	AutoDCR - automatization device configurations and reporting

Version: 0.2.1

Introduction:

	The document communicates the major new features and changes in this release of the AutoDCR. 
	It also documents known problems and workarounds.

Compatible Products:

	This product has been tested on the following platforms or with the following products:
		* Python 2.7.5 and 3.6
		* Cisco IOS

New Features:

	* Added export result of command execution to excel or word.
	  Set export parameter in configurations file or command line. Default value: False - no export.
		
		Values:
		
			excel - export result of search to excel
				
				export available only for command in search type mode: complex and prepared table by regex parent
				
			word - export output of command execution to word template (./data/protocol_template.docx) 

				For create report in word need prepare word template. Example can found in directory 'data'.

				Base requirement:
					Create table for each command with 2 row:
					1 - #command
					2 - Empty


Fixes:

	* Fixed bags in report

Limitations:
	
	* Feature tested only with Cisco IOS