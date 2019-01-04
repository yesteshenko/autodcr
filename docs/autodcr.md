 Name:	AutoDCR - automatization device configurations and reporting

 Author:   Evgen Steshenko yesteshenko@gmail.com
 Year:     2018
 About:    This tools is designed for automatization device configurations and reporting: batch command execution for list of nodes
			with subsequent verification of command output (result)and prepare reports.
 
 General logic:
		Script connect to each node in the csv file: nodes.csv, and execute each command
		in the file: commands.csv. After that, will generated summary report of executions
		each commands on each nodes and full log for each nodes in subfolder 'report'.
 
 Data csv files format:
		Format, rults and examples described in the corresponding file .hlp		
		
 Using:

 1. Set general default configuration in conf file .conf (if need)
 2. Prepare list of nodes and commands in 'data' subfolder
 3. Check installation of Python (tested on Python 2.7.5 and 3.6)
	install additional lib:
	 pip install paramiko
	 pip install netmiko
	 pip install tabulate
	 pip install ConfigParser
	 pip install python-docx
	 pip install openpyxl
	hints: if you have problem with lib: view Python -v and set to pip additional par whith path to lib: sudo pip install --target=/usr/local/lib/python3.6 netmiko 
 4. Execute with default configuration:
		./autodcr.py
	or set in command line:
		usage: autodcr.py [-h] [--version] [-nodes filename]
					 [-commands filename] [-processing type] [-error type]
					 [-searchfail type] [-sort type] [-export type]  [-export type]
 Thanks:
	Natasha Samoylenko 
	https://github.com/natenka
	https://www.gitbook.com/book/natenka/pyneng
	
PS. This is first project in learning python using strategy On Job training 