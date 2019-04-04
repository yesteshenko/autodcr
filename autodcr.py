#!/usr/bin/env python

'''
 Name:	AutoDCR - automatization device configurations and reporting

 Author:   Evgen Steshenko yesteshenko.dev@gmail.com
 Year:     2019
 About:    This tools is designed for automatization device configurations and reporting: batch command execution for list of nodes
			with subsequent verification of command output (result) and prepare reports.
 
 General logic:
		Script connect to each node in the csv file: nodes.csv, and execute each command
		in the file: commands.csv. After that, will generated summary report of executions
		each commands on each nodes and full log for each nodes in subfolder 'report'.
 
 Data csv files format:
		Format, rults and examples described in the docs		
		
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
		usage: autodcr.py [-h] [--version] [-nodes filename] [-nodes_type type]
						  [-nodes_set val val val] [-commands filename]
						  [-conf_template filename] [-conf_template_var json]
						  [-processing type] [-error type] [-searchfail type]
						  [-sort type] [-export type]


 Thanks:
	Natasha Samoylenko 
	https://github.com/natenka
	https://www.gitbook.com/book/natenka/pyneng
	
PS. This is first project in learning python using strategy 'On Job training'
'''

''' Initializing additional libs '''
import sys, os, traceback, logging
import datetime, time
#import ConfigParser
try: 
	from configparser import SafeConfigParser #in Py3.6
except ImportError:
	from ConfigParser import SafeConfigParser #in Py2.7
from lib.ssh_client import *
from lib.utils import *
from lib.export_openxml import * #xlsx_export, docx_export
import argparse
from pprint import pformat, pprint

start_time = datetime.datetime.now()

''' Read configuration '''
BASE_DIR = os.getcwd() + '/'
config_file = BASE_DIR + 'conf/' + __file__.split('/')[-1:][0][:-2] + 'conf'
if os.path.isfile(config_file) :
	config = SafeConfigParser()
	config.read(config_file)
else :
	print('{}[Err]{} Configuration file: {} does not exist'.format(bcolors.FAIL, bcolors.ENDC, config_file))
	exit(0)
	
#Set logging
logstatus =  config.get('general', 'log')
log_filename = __file__.split('/')[-1:][0][:-2] + 'log'

if config.get('general', 'logdir') == '':
	log_ffilename = BASE_DIR + 'log/' + log_filename
else:
	log_ffilename = config.get('general', 'logdir') + log_filename

loglevel = getattr(logging, config.get('general', 'loglevel').upper())
try:
	logging.basicConfig(filename=log_ffilename, level=loglevel, filemode="w" )# add filemode="w" to overwrite
except IOError:
	os.mkdir('log')
	logging.basicConfig(filename=log_ffilename, level=loglevel, filemode="w" )

''' Parse script arguments '''
argparser = argparse.ArgumentParser(description='This tools is designed for automatization device configurations and reporting: batch command execution for list of nodes with subsequent verification of command output (result) and prepare reports.')
argparser.add_argument('--version', action='version', version='%(prog)s 0.3.5')
argparser.add_argument("-nodes", action="store", dest="nodes_filename", metavar='filename', default=config.get('general', 'nodes'), required=False, help="list of nodes with connections parameters (default: {})".format(config.get('general', 'nodes')))
argparser.add_argument("-nodes_type", action="store", dest="nodes_type", metavar='type', default=config.get('general', 'nodes_type'), required=False, help="type of config file for import nodes:\n for CSV format - csv,\n for YAML format - yaml (default: {})".format(config.get('general', 'nodes_type')))
argparser.add_argument("-nodes_set", action="store", metavar='val', dest="nodes_set", required=False, nargs=3, help='Set of values of nodes from yaml data file. Arguments: 1st: group, 2nd: node_name or all, 3rd: parameners')
argparser.add_argument("-commands", action="store", dest="commands_filename", metavar='filename', default=config.get('general', 'commands'), required=False, help="list of commands for executing (default: {})".format(config.get('general', 'commands')))
argparser.add_argument("-conf_template", action="store", dest="conf_template", metavar='filename', default=config.get('general', 'conf_template'), required=False, help="configurations template (default: {})".format(config.get('general', 'conf_template')))
argparser.add_argument("-conf_template_var", action="store", dest="conf_template_var", metavar='json', default=config.get('general', 'conf_template_var'), required=False, help="variables for configurations template in json format: 'json' (default: {})".format(config.get('general', 'conf_template_var')))
argparser.add_argument("-processing", action="store", dest="processing", metavar='type', choices=['True', 'False'], default=config.get('general', 'multiprocessing_exec'), required=False, help="logic of processing nodes: multiprocessing = True, singlrocessing (exec in queue) = False (default: {})".format(config.get('general', 'multiprocessing_exec')))
argparser.add_argument("-error", action="store", dest="error", metavar='type', choices=['True', 'False'], default=config.get('general', 'cmd_exec_err_logic'), required=False, help="executing commands logic when error (fail) found: stop execution commands = True, continue execution commands = False (default: {})".format(config.get('general', 'cmd_exec_err_logic')))
argparser.add_argument("-searchfail", action="store", dest="searchfail", metavar='type', choices=['True', 'False'], default=config.get('general', 'cmd_exec_searchfail_logic'), required=False, help="executing commands logic when fail search value of output: stop execution commands = True, continue execution commands = False (default: {})".format(config.get('general', 'cmd_exec_searchfail_logic')))
argparser.add_argument("-sort", action="store", dest="sort", metavar='type', choices=['node', 'command'], default=config.get('general', 'report_sort'), required=False, help="Sort by node = node (by default),  sort by command = command (default: {})".format(config.get('general', 'report_sort')))
argparser.add_argument("-export", action="store", dest="export", metavar='type', choices=['excel', 'word', 'False'], default=config.get('general', 'export'), required=False, help="Set export result. Values: False - no export; excel - export result of search to excel (only command in search type mode: complex); word - export output of command execution to word template (./data/protocol_template.docx)  (default: {})".format(config.get('general', 'export')))
args = argparser.parse_args()
logging.debug('Arguments list:  %s' % (args))
#If need to print DEBUG to console:
#logging.getLogger().setLevel(logging.DEBUG)	

#Disable logging:
if logstatus == 'False' and sys.version_info[0] == 2:
	logging.disable(config.get('general', 'loglevel'))
	print ('!Log is disabled! Log=' + logstatus)
else:
	#For pyton v3 do not disable logging!!! it is bug (getting error  in isEnabledFor if self.manager.disable >= level: TypeError: '>=' not supported between instances of 'str' and 'int')!!!
	logging.basicConfig(filename=log_ffilename, level='INFO', filemode="w" )

print ('Script running on Python version: {}'.format(sys.version_info[0]))
logging.info ('Script running on Python version: {}'.format(sys.version_info[0]))
logging.info ("Start working: %s" % (datetime.datetime.now()))
print ("Start working: %s" % (datetime.datetime.now()))
logging.info("\n\n--------- Configuration: -------------")
for section_name in config.sections():
	logging.debug('Section:  %s' % (section_name))
	logging.debug('  Options: %s' % (config.options(section_name)))
	for name, value in config.items(section_name):
		logging.debug('  %s = %s' % (name, value))
logging.info("\n\n--------- ------------- -------------")

''' Annanouncing global variables '''
nodes_file = os.path.normpath(BASE_DIR + 'data/' + args.nodes_filename)
commands_file = os.path.normpath(BASE_DIR + 'data/' + args.commands_filename)
cmd_exec_logic = {
		'multiprocessing_exec': eval(args.processing),
		'cmd_exec_err_logic': eval(args.error),
		'cmd_exec_searchfail_logic': eval(args.searchfail)
}
results = []
max_process = int(config.get('general', 'max_process'))
server_par = {
		'logstatus': eval(config.get('general', 'log')),
		'port': int(config.get('server', 'port')),
		'host': config.get('server', 'host')
}

if config.get('server', 'server') == 'True': 
	from lib.rest_appl import *
	server(BASE_DIR, nodes_file, args, cmd_exec_logic, max_process, server_par)

else:
	''' Read and load data '''
	if args.nodes_type == 'yaml':
		nodes_data = get_data_yaml(nodes_file, args.nodes_set)
		nodes_list_dist = nodes_data.get('dict')
		nodes_list = nodes_data.get('list')
	else:
		nodes_list = get_data(nodes_file, 'nodes')
	if args.nodes_type == 'csv': nodes_list_dist = lits_to_dict(nodes_list)
	commands_list = get_data(commands_file, 'commands')
	if args.conf_template: commands_list = parce_conf_template(os.path.normpath(BASE_DIR + 'data/' + args.conf_template), commands_list, args)		
	''' Transformation list to dictionary '''
	commands_list_dist = lits_to_dict(commands_list)	
	
	''' Executing commands '''
	if cmd_exec_logic.get('multiprocessing_exec'):
		results =  conn_processes(connect_ssh, nodes_list_dist, commands_list_dist, cmd_exec_logic, max_process)
	else:
		for device in nodes_list_dist:
			results.append(connect_ssh(device, commands_list_dist, cmd_exec_logic))
			
	logging.debug('Result of exec cmd on all nodes: %s' % (pformat(results)))

	''' Reporting '''
	print ('Start report:')
	logging.info('Start reporting:.....')
	print_full_report_to_file(results, BASE_DIR)
	prepare_summary_report(results, BASE_DIR, args.sort, nodes_list[1:], commands_list[1:])
	if args.export == 'excel': xlsx_export(results, BASE_DIR)
	if args.export == 'word': docx_export(results, BASE_DIR)

	logging.info('End of executing script, time: %s' % (datetime.datetime.now() - start_time))
	print('End of executing script, time: %s' % (datetime.datetime.now() - start_time))
