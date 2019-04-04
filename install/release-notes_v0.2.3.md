Release Note

	AutoDCR - automatization device configurations and reporting

Version: 0.2.3

Introduction:

	The document communicates the major new features and changes in this release of the AutoDCR. 
	It also documents known problems and workarounds.

Compatible Products:

	This product has been tested on the following platforms or with the following products:
		* Python 2.7.5 and 3.6
		* Cisco IOS, Linux OS

New Features:

	* Added possibility use result report of previous command for send to shell OS command
	  
	  Use:
		Set value 'os_exec' in parameter: 'cmd_type' for command in command.csv file.
		Add in body of command:
			<> 			- in command means use result report of previous command for send to shell OS command (mandatory)
			{command} 	- will be replaced by previous command (oprional)
			{nodename} 	- will be replaced by current node name (oprional)
			{ip} 		- will be replaced by current node ip (oprional)

Limitations:
	
	* Feature tested only with Cisco IOS