''' Initializing additional libs '''
import sys, os, traceback, logging
import datetime, time
import csv, yaml
import re, json
from tabulate import tabulate
from pprint import pformat, pprint
import clitable
#import textfsm.clitable as clitable
import textfsm

''' Annanouncing global variables '''
CLI_error_cisco = 'Invalid|Unknown|is not a valid|Cannot|not exist|already exists|are the same|was missing|Could not|Error|not have permission|try again later|Insufficient disk space'

def get_data(file, type, delimiter=';'):
	''' 
	Read and load data (with simple checking syntax)
		Arg:
			file: path files for load data
			type: type of load data
	'''
	try:
		with open(file, 'r') as csvfile:
			data = list(csv.reader(csvfile, delimiter=';'))
		logging.debug('%s:  %s' % (type, pformat(data)))
	except IOError:
		print('[Err] {} list file: {} does not exist'.format(type, file))
		exit(1)	
		
	#Checking format
	check_var = ''
	if type == 'nodes': check_var = 'nodename'
	if type == 'commands': check_var = 'cmdname'
	if data[0][0] != check_var:
		print('\nSomething wrong in {} file syntax, try to set delimiter: \",\" '.format(type))
		with open(file, 'r') as csvfile:
			data = list(csv.reader(csvfile, delimiter=','))
		if data[0][0] != check_var:
			print('\nSomething wrong in {} file syntax, end work'.format(type))
			exit()
	logging.debug('%s:  %s' % (type, pformat(data)))
	#Delete empty lines
	data = filter(bool, data)
	result = data
	return result

def get_data_yaml(file, args):
	''' 
	Read and load data (with simple checking syntax)
		Arg:
			file: path files for load data
			args: main program command arguments
	'''
	try:
		with open(file) as f:
			yaml_data = yaml.load(f)
		logging.debug('%s:  %s' % ('nodes', pformat(yaml_data)))
	except IOError:
		print('[Err] {} list file: {} does not exist'.format('nodes', file))
		exit(1)
	
	if args.nodes_set == None:
		print('Check paramener: nodes_set.\n Requared 3 arguments:\n  1st: group,\n  2nd: node_name or all,\n  3rd: parameners\n Given: {}'.format(args.nodes_set))
		exit()	
	if len(args.nodes_set) != 3:
		print('Check paramener: nodes_set.\n Requared 3 arguments:\n  1st: group,\n  2nd: node_name or all,\n  3rd: parameners\n Given: {}'.format(args.nodes_set))
		exit()
		
	requested_nodes_group = args.nodes_set[0]
	requested_nodes = args.nodes_set[1]
	requested_nodes_param = args.nodes_set[2]
	nodes_list_dist = []
	if requested_nodes == 'all':
		for node in yaml_data.get(requested_nodes_group):
			nodes_dist = {'nodename' : node, 'ip' : yaml_data.get(requested_nodes_group).get(node)}
			nodes_dist.update(yaml_data.get(requested_nodes_param))
			nodes_list_dist.append(nodes_dist)
	else:
		nodes_dist = {'nodename' : requested_nodes, 'ip' : yaml_data.get(requested_nodes_group).get(requested_nodes)}
		nodes_dist.update(yaml_data.get(requested_nodes_param))
		nodes_list_dist.append(nodes_dist)
	
	return {'list': dict_to_lits(nodes_list_dist),'dict': nodes_list_dist}

def parce_conf_template(file, commands_list, args):
	''' 
	Read and parce configuration template
		Arg:
			file: path files for load conf_template_file
			commands_list: list of commands
			args: main program command arguments  
	'''
	try:
		with open(file) as open_file:
			alldata = open_file.read()
	except IOError:
		print('[Err] Config template file: {} does not exist'.format(file))
		exit(1)
	for cmd_index, command in enumerate(commands_list):
		if re.match('Config', command[0]) != None: 
			commands_list[cmd_index][1] = re.sub('\n', ',', alldata)
			break

	if args.conf_template_var:
		dict_var = json.loads(args.conf_template_var)
		for cmd_index, command in enumerate(commands_list):
			search = re.match('Config', command[0])
			if re.match('Config', command[0]) != None:
				for var in dict_var:
					commands_list[cmd_index][1] = re.sub('\{'+var+'\}', dict_var.get(var), command[1])
				break
	return commands_list
	
def lits_to_dict(list, name=True):
	'''
	Transformation list table to list whith dictionary
		Arg:
			list: list for transformation
			name: 	True -> with nodename, first collumb in list table (default)
					False -> without nodename
	'''
	result = []
	for index, line in enumerate(list[1:]):
		if name:
			result.append(dict(zip(list[0],line)))
		else:
			result.append(dict(zip(list[0][1:],line[1:])))
	logging.debug('Transformation list table to list whith dictionary:\n%s' % (pformat(result)))
	return result

def dict_to_lits(dict, name=True):
	'''
	Transformation list of dict to list of list
		Arg:
			list: dict for transformation
			name: 	True -> with nodename, first collumb in list table (default)
					False -> without nodename
	'''
	result = []
	header = ['nodename','ip','username','password','secret','device_type']
	result.append(header)
	for d_item in dict:
		list = []
		for h_item in header:
			list.append(d_item.get(h_item))
		result.append(list)
	return result
	
def print_full_report_to_file(results, BASE_DIR):
	'''
	Print result of executing command to log file
		Arg:
			results: List with all data
			BASE_DIR: base directory of script
	'''
	print ('Generation full report.....')
	logging.info('Generation full report.....')
	for node in results:
		output_filename = os.path.normpath(BASE_DIR + "report/" + list(node.keys())[0] + "_{}.log".format(time.strftime("%Y%m%d%H%M%S")))
		logging.debug('Open file for write: %s' % (output_filename))
		logging.debug('in data: %s' % (node))
		output_file_handle = open(output_filename, "w") # File being opened in write mode
		output_file_handle.write("Start working: %s \n" % (datetime.datetime.now()))
		output_file_handle.write('==========================================\n')
		output_file_handle.write( 'Node name: {}\n'.format(list(node.keys())[0]))
		output_file_handle.write( '------------------------------------------\n')
		for output in node.get(list(node.keys())[0]):
			if output.get('output') == None: output['output'] = 'Command did not executed'
			logging.debug('output data: %s' % (pformat(output)))
			output_file_handle.write( '< - Command: {} output start ->\n'.format(output.get('command')))
			output_file_handle.write( output.get('output'))
			output_file_handle.write( '\n< - Command: {} output end ->\n'.format(output.get('command')))
		output_file_handle.write( '==========================================\n')
		
		# Close both file handles
		output_file_handle.close()
	print ('Full report generated')
	logging.info('Full report generated')
	
def conv_tuple_list(results):
	'''
	Convert result from tuple to list
		Arg:
			results: list with results
	'''
	result_list = []
	for result in results:
		result_list.append(list(result))
	return result_list
	
def check_tuple(result):
	'''
	Check for type of result and if it is tuple convert
		Arg:
			result: list with results
	'''
	if sys.version_info[0] == 2: 
		if isinstance(result[0], basestring): # or isinstance(result[0], unicode) 'unicode for list or tuple tabulate work well'
			conv_tuple_list(result)
			#result_list.append(result)
			#result = result_list
	if sys.version_info[0] == 3: 
		if isinstance(result[0], str): # or isinstance(result[0], unicode) 'unicode for list or tuple tabulate work well'
			conv_tuple_list(result)
			#result_list.append(result)
			#result = result_list
	return result
	
def check_output(command_result, export = False):
	'''
	Parse result of executing command. Check for error, search values. And generate result for reporting
		Arg:
			command_result: command output
			export: True - generate result for exporting
	'''
	# reg fof match host [\w\-\(\)]+#|> or ^.*#$ -> match empry promt of ^.*#.*$ -> match promt whith 
	result = '' 
	search = ''
	logging.debug('incoming data for check_output: %s' % (pformat(command_result)))
	result = re.findall(CLI_error_cisco, command_result.get('output'))
	logging.debug('\nCheck for error (Unknown command|Invalid input or ...): in data:\n <-\n%s\n-> \n, result: %s\n' % (command_result.get('output'), ''.join(result)))
	if len(result) > 0: return 'Error exec cmd [Err: {}]'.format(command_result.get('output'))
	search = command_result.get('search')
	if command_result.get('search') == '': return 'No search values'
	if command_result.get('search') == 'promt': search = '.*#$'
	if command_result.get('search') == 'request': search = '.*: $'
	if command_result.get('search') == 'confirm': search = '.* \[.*\]'
	try:
		result = re.findall(search, command_result.get('output'))
	except:
		print('[Err] invalid regex expression: {}'.format(search))
	
	header = []
	delim = ''
	header = re.findall('P<(\w+)>', search)
	logging.debug('Header of search: %s' % (pformat(header)))
	#logging.debug('\nSearch {} in output of cmd {} \n, result: {}\n'.format(command_result.get('search'), command_result.get('output'), ''.join(result)))
	result_marker = command_result.get('result_marker')
	if result_marker == None or result_marker == '': 
		result_marker = ['','']
	else:
		result_marker = result_marker.split(',')
	logging.debug('Result of search: %s' % (pformat(result)))
	if len(result) > 0:
		if len(header) == 1: delim = ':'
		if command_result.get('last_val') == 'last' and len(result) >= 2: result = result[-1]
		if command_result.get('search_type') == 'simple':
			if len(header) <= 1:
				if isinstance(result[0], tuple) and len(result) == 1:
					return '{} [{}{} {}]'.format(result_marker[0], ''.join(header), delim, ' '.join(result[0]))
				elif isinstance(result[0], list) == False and isinstance(result[0], tuple) == False:
					return '{} [{}{} {}]'.format(result_marker[0], ''.join(header), delim, ' '.join(result))
				else:
					command_result['search_type'] = 'complex'
		if command_result.get('search_type') == 'TextFSM':
			attributes = {'Command': command_result.get('command') , 'Platform': command_result.get('device_type')}
			logging.debug('attributes for TextFSM: {}'.format(pformat(attributes)))
			logging.debug('output for TextFSM: {}'.format(pformat(command_result.get('output'))))
			try:
				cli_table.ParseCmd(command_result.get('output'), attributes)
				header = list(cli_table.header)
				result = [list(row) for row in cli_table]
			except Exception as e: #clitable.CliTableError:
				pprint ('\nOutput formating  failed! {}'.format(e))
				result = [e]
			
			logging.debug('header of TextFSM parce: {}'.format(pformat(header)))
			logging.debug('result of TextFSM parce: {}'.format(pformat(result)))
			#print (cli_table)
			#template = open('/opt/cisco/scripts/batch_cmd_exec/TextFSMtemplates/cisco_ios_show_clock.template')
			#fsm = textfsm.TextFSM(template)
			#textfsmresult = fsm.ParseText(command_result.get('output'))
			#print(textfsmresult)
			
			if export: 
				result.insert(0, header)
				return result
			return '{} [result:\n\t\t\t command:{}\n\t\t\t {}]'.format(result_marker[0], command_result.get('command'), re.sub('\n',  '\n\t\t\t', tabulate(result, headers=header, tablefmt='grid')))			
		if command_result.get('search_type') == 'complex':
			#result_header = ['Coll'] * (len(result))
			logging.debug('Result type is: {}'.format(type(result[0])))
			
			result = conv_tuple_list(result)

			#pprint(result.insert(0, header))
			logging.debug('Result after add to list: {}'.format(pformat(result)))
			if export: 
				result.insert(0, header)
				return result
			return '{} [result:\n\t\t\t command:{}\n\t\t\t {}]'.format(result_marker[0], command_result.get('command'), re.sub('\n',  '\n\t\t\t', tabulate(result, headers=header, tablefmt='grid')))
		elif not command_result.get('search_type') == 'simple':
			if len(header) == 1 :
				return '{} [{}{} {}]'.format(result_marker[0], ''.join(header), delim, len(result))
			else:
				return '{} [search: {}, count: {}]'.format(result_marker[0], command_result.get('search'), len(result))			
	if command_result.get('output') == 'Command did not executed': return 'Command did not executed, script stopped'
	return '{} (Fail find search value)'.format(result_marker[1])
	
def parse_output_cmds(output_cmds):
	'''
	Parse result of executing commands for node
		Arg:
			output_cmds: List with all commands
	'''
	result = []
	result.append(['CmdName', 'Result'])
	logging.debug('incoming data for parse_output_cmds: %s' % (output_cmds))
	for output in output_cmds:
		logging.debug('output data of cmd: %s' % (pformat(output)))
		#result[output.get('cmdname')] = check_output(output) # it is for dict
		result.append([output.get('cmdname'), check_output(output)])
	return result		

def reassembing_results(results, nodes_list, commands_list):
	'''
	Reassembing result of executing command for generating report with report sort by command
		Arg:
			results: List with all data
			nodes_list: list of nodes
			commands_list: list of commands
	'''
	reassemb_list = []
	summary_result = {}	
	for node in results: #enumerate(nodes_list)
		summary_result[list(node.keys())[0]] = parse_output_cmds(node.get(list(node.keys())[0]))[1:]
	logging.debug('summary_result: %s' % (pformat(summary_result)))
	
	for cmd_index, command in enumerate(commands_list):
		cmd_res_list = []
		for node_index, node in enumerate(nodes_list):
			cmd_res_list.append([node[0], summary_result.get(node[0])[cmd_index][1]])
		reassemb_list.append({command[0]:  cmd_res_list})
	logging.debug('reassemb_list: %s' % (pformat(reassemb_list)))
	return reassemb_list
	
def prepare_summary_report(results, BASE_DIR, report_sort, nodes_list, commands_list):
	'''
	Print summary result of executing command to log file
		Arg:
			results: List with all data
			BASE_DIR: base directory of script
			report_sort: type of report sort
			nodes_list: list of nodes
			commands_list: list of commands
	'''
	result_table = []
	print ('Start preparing summary report.....')
	logging.info('Start preparing summary report.....')	
	summary_report = 'Summary report:\n'
	summary_report = summary_report + '\n==========================================\n'

	if report_sort == 'command':
		result_table_header = ['nodename', 'Result']
		reassemb_list = reassembing_results(results, nodes_list, commands_list)
		
		for cmd in reassemb_list:
			summary_report = summary_report + '\n   Commands name: {}\n'.format(list(cmd.keys())[0])
			summary_report = summary_report + '\n------------------------------------------\n'
			result_table = tabulate(cmd.get(list(cmd.keys())[0]), headers=result_table_header, tablefmt="pipe")
			logging.debug('result_table of cmd executions: %s' % (result_table)) #print(result_table)
			summary_report = summary_report + result_table + '\n'
			summary_report = summary_report + '\n==========================================\n'	
	else:
		for node in results:
			summary_report = summary_report + '\n   Node name: {}\n'.format(list(node.keys())[0])
			summary_report = summary_report + '\n------------------------------------------\n'
			#summary_report = summary_report + str(parse_output_cmds(node.get(list(node.keys())[0]))) + "\n"
			result_table = tabulate(parse_output_cmds(node.get(list(node.keys())[0])), headers='firstrow', tablefmt="pipe")
			logging.debug('result_table of cmd executions: %s' % (result_table)) #print(result_table)
			summary_report = summary_report + result_table + '\n'
			summary_report = summary_report + '\n==========================================\n'
	#fix output tabulate if result table very big
	summary_report = re.sub( ':(-){50,}', ':' + '-'*50, summary_report)
	summary_report = re.sub( '( ){50,}', '', summary_report)
	output_filename = os.path.normpath(BASE_DIR + "report/summary_report_{}.log".format(time.strftime("%Y%m%d%H%M%S")))
	output_file_handle = open(output_filename, "w") # File being opened in write mode
	output_file_handle.write(summary_report)	
	# Close both file handles
	output_file_handle.close()
	print ('Summary report prepared')
	logging.info('Summary report prepared')		
	print (summary_report)

cli_table = clitable.CliTable('index', 'templates')