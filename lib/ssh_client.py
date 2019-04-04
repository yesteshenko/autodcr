''' Initializing additional libs '''
import multiprocessing, os, subprocess, threading, sys
from netmiko import ConnectHandler
import logging, re
from lib.utils import check_output, parce_node_conf_template, bcolors, get_result
from pprint import pformat, pprint
import subprocess as sp
from tabulate import tabulate
import copy
import datetime, time

def chech_fail_exec(command, cmd_exec_logic):
	'''
	Check for error or search in output of command executing
		Arg:
			command: command dict
			cmd_exec_logic: logic for check
	'''
	logging.debug('Checking exec cmd: %s' % (pformat(command)))
	result = check_output(command)
	if cmd_exec_logic.get('cmd_exec_err_logic'):
		search = re.match('.*Error exec cmd', result)
		if search != None: 
			logging.debug('Found error on executing command:\n%s' % (pformat(result)))
			#print ('Found error on executing command:\n%s' % (result))
			return True
	if cmd_exec_logic.get('cmd_exec_seachfail_logic'):
		search = re.match('.*Fail find search value', result)
		if search != None:
			logging.debug('Fail find search value of executing command')
			return True		
	return False
	
def get_expect_string(command, current_prompt, device_type):
	'''
	Transform search string to regex pattern
	!!! tested for cisco_ios!!!
		Arg:
			command: command dict
			current_prompt: current prompt on device
			device_type: device type
	'''
	if command.get('expect'):
		print ("catch: {}".format(command.get('expect')))
		return command.get('expect')
	if device_type == 'cisco_ios' or device_type == 'cisco_xr' or device_type == 'cisco_xe':
		if command.get('search') == 'prompt': return current_prompt #'.*\#$'
		if command.get('search') == 'prompt_cnf': return '.*\(\S+\)\#$'
		if command.get('search') == 'request': return '.*: $'
		if command.get('search') == 'confirm': return '.* \[.*\]'
		return '.*#$'
	#if device_type == 'linux': return '# $'
	if command.get('search') == 'prompt': return current_prompt
	return ''
	# .* (not always work correctly) <= no matter what get, or restrict expect value =>  '.*#($|\s+)'
	
def connect_ssh(device_dict, commands_set, cmd_exec_logic, fileno=None):
	'''
	Connect to device and execute command list
	!!! tested for cisco_ios!!!
		Arg:
			devices: parameters of device (dict)
			queue: list of result
			commands_set: list of commands
			cmd_exec_logic: logic of execution
	'''
	# We need to copy dict in list of command (create new object), otherwise we will get last commands set (result) for all nodes (change same object of commands)
	if not fileno == None: sys.stdin = os.fdopen(fileno)
	commands = copy.deepcopy(commands_set)
	queue = {}
	nodename = device_dict.get('nodename')
	del(device_dict['nodename'])
	print ("%s[%s]%s Connection to device %s" % (bcolors.HEADER, nodename, bcolors.ENDC, device_dict['ip']))
	logging.info("Connection to device %s" % device_dict['ip'])
	try:
		ssh = ConnectHandler(**device_dict)
	except Exception as e:
		logging.debug('\nConnect failed! {}'.format(e))
		print('\n\033[95m[{0}]\033[0m [\033[91mErr\033[0m] Connect failed! {1}'.format(nodename, e))
		logging.info ("Stop executing commands")
		print('\n\033[95m[{0}]\033[0m [\033[91mErr\033[0m] Stop executing commands'.format(nodename))
		failed_dic = [{'cmdname': 'Err', 'output': str(e), 'search': '' }]
		queue[nodename] = failed_dic
		return queue
	ssh.enable()
	for cmd_index, command in enumerate(commands):
		logging.debug('\n $command=:\n{} '.format(pformat(command)))
		#Checking command
		if command.get('command') == None:
			logging.debug('\nSomething wrong in command syntax\'s! Incoming config for current command:\n{} '.format(pformat(command.get('command'))))
			print('\n\033[95m[{0}]\033[0m [\033[91mErr\033[0m] Something wrong in command syntax\'s! Incoming config for current command:\n{1} '.format(nodename, pformat(command.get('command'))))
			logging.info ("Stop executing commands")
			print('\n\033[95m[{0}]\033[0m [\033[91mErr\033[0m] Stop executing commands'.format(nodename))
			failed_dic = [{'cmdname': 'Err', 'output': 'Something wrong in command syntax', 'search': '' }]
			queue[nodename] = failed_dic
			return queue			
		cmd=''
		cmd_list = []
		cmd_var_search = []
		#build-in variables
		cmd_var_search = re.findall('\{\}', command.get('command'))
		command['command'] = re.sub('\{nodename\}', nodename, command.get('command'))
		command['command'] = re.sub('\{nodeip\}', device_dict['ip'], command.get('command'))
		command['command'] = re.sub('\{datetime\}', time.strftime("%Y%m%d%H%M%S"), command.get('command'))
		command['command'] = re.sub('\{date\}', time.strftime("%Y%m%d"), command.get('command'))
		command['search'] = re.sub('\{nodename\}', nodename, command.get('search'))
		command['search'] = re.sub('\{nodeip\}', device_dict['ip'], command.get('search'))
		command['search'] = re.sub('\{datetime\}', time.strftime("%Y%m%d%H%M%S"), command.get('search'))
		command['search'] = re.sub('\{date\}', time.strftime("%Y%m%d"), command.get('search'))		
		
		command['device_type']  =  device_dict['device_type']
		
		if command.get('delay_factor') == '': 
			logging.debug("set def delay_factor")
			command['delay_factor'] = '1'
		if cmd_var_search:
			result = re.findall(commands[cmd_index-1].get('search'), commands[cmd_index-1].get('output'))
			if result:
				cmd_parrent = command.get('command')
				for var_index, var in enumerate(result):
					cmd = cmd_parrent.format(var)
					if var_index == 0: 
						commands[cmd_index]['command'] = cmd
					else:
						cmd_dic = {}
						cmd_dic = command.copy()
						cmd_dic['command'] = cmd
						cmd_dic['cmdname'] = cmd_dic.get('cmdname') + '(' + str(var_index) + ')'
						commands.insert(cmd_index + var_index, cmd_dic)
				logging.debug('\nNew command list:\n' + pformat(commands))
			else:
				logging.info ("Stop executing commands")
				print ("%s[%s]%s [\033[91mErr\033[0m] Stop executing commands list on command  %s on device: %s:" % (bcolors.HEADER, nodename, bcolors.ENDC, command.get('command'), device_dict['ip']))
				logging.info ("Stop executing commands list on command  %s on device: %s:" % (command.get('command'), device_dict['ip']))
				break
		
		cmd_varlist_search = []
		cmd_varlist_search = re.findall('\{\$\S+\}', command.get('command'))
		if cmd_varlist_search:
			table = get_result(commands[cmd_index-1])
			#check if result is list and not empty
			if len(table)>=2 and type(table) == list:
				cmd_parrent = command.get('command')
				for varline_index, varline in enumerate(table):
					if varline_index == 0: continue
					new_cmd = cmd_parrent
					for var_index, var in enumerate(varline):
						if var_index == 0: continue
						new_cmd = re.sub('\{\$' + table[0][var_index] + '\}', var, new_cmd)
					if varline_index == 1: 
						commands[cmd_index]['command'] = new_cmd	
					else:
						cmd_dic = {}
						cmd_dic = command.copy()
						cmd_dic['command'] = new_cmd
						cmd_dic['cmdname'] = cmd_dic.get('cmdname') + '(' + str(varline_index) + ')'
						commands.insert(cmd_index + varline_index, cmd_dic)
				logging.debug('\nNew command list:\n' + pformat(commands))
			else:
				logging.info ("Stop executing commands")
				print ("%s[%s]%s [\033[91mErr\033[0m] Stop executing commands list on command  %s on device: %s:" % (bcolors.HEADER, nodename, bcolors.ENDC, command.get('command'), device_dict['ip']))
				logging.info ("Stop executing commands list on command  %s on device: %s:" % (command.get('command'), device_dict['ip']))
				break						
		print ("%s[%s]%s Try to execute command: %s on device: %s:" % (bcolors.HEADER, nodename, bcolors.ENDC, command.get('command'), device_dict['ip']))
		logging.info ("Try to execute command: %s on device: %s:" % (command.get('command'), device_dict['ip']))
		
		cmd = command.get('command')

		if command.get('cmd_type') == 'usr_req':
			usr_req = raw_input('{}[{}]{} {}{}{}'.format(bcolors.HEADER, nodename, bcolors.ENDC, bcolors.WARNING, command.get('command'), bcolors.ENDC))
			commands[cmd_index+1]['search'] = re.sub('\{usr_req\}', usr_req, commands[cmd_index+1]['search'])
			commands[cmd_index]['output'] = usr_req
			commands[cmd_index]['search'] = usr_req
			commands[cmd_index]['search_type'] = 'simple'
		if command.get('cmd_type') == 'choose_req':
			print('{}[{}]{} {}{}{}'.format(bcolors.HEADER, nodename, bcolors.ENDC, bcolors.WARNING, command.get('command'), bcolors.ENDC))
			table = get_result(commands[cmd_index-1])
			if len(table)>=2:
				print(tabulate(table, headers='firstrow', tablefmt="pipe"))
				while True:
					usr_input = raw_input('{}[{}]{} {}Enter number of line:{}'.format(bcolors.HEADER, nodename, bcolors.ENDC, bcolors.WARNING, bcolors.ENDC))
					try:
						usr_input = int(usr_input)
					except:
						print('{}[{}]{} {}Entered not number of line, please enter number{}'.format(bcolors.HEADER, nodename, bcolors.ENDC, bcolors.WARNING, bcolors.ENDC))
						continue
					if usr_input in range(0, len(table)-1): 
						break
					else:
						print('{}Enter number of line in range {}{}'.format(bcolors.WARNING, range(0, len(table)-1), bcolors.ENDC))
				var_dict=dict(zip(table[0],table[usr_input+1]))
				for var in var_dict:
					if var == 'N': continue
					commands[cmd_index+1]['command'] = re.sub('\{' + str(var) + '\}', var_dict.get(var), commands[cmd_index+1]['command'])
				command['output'] = str(usr_input)
			else:
				logging.info ("Stop executing commands")
				print ("%s[%s]%s [\033[91mErr\033[0m] Stop executing commands list on command  %s on device: %s:" % (bcolors.HEADER, nodename, bcolors.ENDC, command.get('command'), device_dict['ip']))
				logging.info ("Stop executing commands list on command  %s on device: %s:" % (command.get('command'), device_dict['ip']))
				break
				
		if command.get('command') == 'timeout':
			print("%s[%s]%s Start timeout of executing script: %s" % (bcolors.HEADER, nodename, bcolors.ENDC, command.get('delay_factor')))
			time.sleep(int(command.get('delay_factor')))
			command['output'] = 'Timeout: %ssec' % (command.get('delay_factor'))
			print("%s[%s]%s Continue executing script" % (bcolors.HEADER, nodename, bcolors.ENDC,))
		if command.get('command') == 'enter': cmd = '\n'
		if command.get('cmd_type') == 'conf_tpl' and  not command.get('command') == '':
			command['command'] = parce_node_conf_template(nodename, command)
			command['cmd_type']  = 'conf_set'
		if command.get('cmd_type') == 'conf_enter': 
			command['output']  =  ssh.config_mode()
		elif command.get('cmd_type') == 'conf_exit': 
			command['output']  =  ssh.exit_config_mode()
		elif command.get('cmd_type') == 'conf_set':
			cmd_list = command.get('command').split(',')
			#for debug
			#print ('Find prompt is %s' % (ssh.find_prompt()))
			#prompt = ssh.send_command('\n', strip_prompt = False, strip_command = False, expect_string = '.*', auto_find_prompt=False)
			#print ('Current prompt is %s' % (prompt))
			ssh.set_base_prompt()
			command['output']  =  ssh.send_config_set(cmd_list, strip_prompt = False, strip_command = False, delay_factor = int(command.get('delay_factor')))#.encode('ascii').decode('utf-8')
		elif command.get('cmd_type') == 'os_exec':
			cmd = re.sub('\<\>', check_output(commands[cmd_index-1]), command.get('command'))
			#result = re.findall(commands[cmd_index-1].get('search'), commands[cmd_index-1].get('output'))
			#cmd = re.sub('\<\>', tabulate(result, headers=re.findall('P<(\w+)>', commands[cmd_index-1].get('search')), tablefmt='html'), command.get('command'))
			cmd = re.sub('\{command\}', commands[cmd_index-1].get('command'), cmd)
			cmd = re.sub('\{nodename\}', nodename, cmd)
			cmd = re.sub('\{ip\}', device_dict['ip'], cmd)
			cmd = re.sub('\n', '\n\r', cmd)
			#print (cmd)
			command['output']  =  sp.check_output(cmd, shell=True)
		elif command.get('output') == None:
			#print (ssh.find_prompt())
			#print command.get('expect')
			current_prompt = '.*'
			if not command.get('expect'):
				try:
					current_prompt = ssh.find_prompt()
					logging.debug('Current prompt is %s' % (ssh.find_prompt()))
				except Exception as e:
					logging.debug('\nUnable to find prompt! {}'.format(e))
					#print('\n[{0}] Unable to find prompt! {1}'.format(nodename, e))
				expect_prompt =  get_expect_string(command, current_prompt, device_dict['device_type'])
				if expect_prompt == "":
					try:
						command['output']  =  ssh.send_command(cmd, strip_prompt = False, strip_command = False, delay_factor = int(command.get('delay_factor')))#.
					except Exception as e:
						logging.debug('\nError {}'.format(e))
						print('\n{}[{}]{} Error {}'.format(bcolors.HEADER, nodename, bcolors.ENDC, e))
						break
			else:
				expect_prompt = command.get('expect')
			
			logging.debug('Expect prompt = %s' % (expect_prompt))
			try:
				command['output']  =  ssh.send_command(cmd, strip_prompt = False, strip_command = False, delay_factor = int(command.get('delay_factor')), expect_string = expect_prompt, auto_find_prompt=False)#.encode('ascii').decode('utf-8')
			except Exception as e:
				logging.debug('\nError! {}'.format(e))
				print('\n{}[{}]{} Error {}'.format(bcolors.HEADER, nodename, bcolors.ENDC, e))
				break
				
		logging.info("Checking executing commands logic:")
		if cmd_exec_logic.get('cmd_exec_err_logic') or cmd_exec_logic.get('cmd_exec_searchfail_logic'):
			print('{}[{}]{} Check command {} for error'.format(bcolors.HEADER, nodename, bcolors.ENDC, command.get('command')))
			result = chech_fail_exec(command, cmd_exec_logic)
			if result: 
				logging.info ("Stop executing commands")
				print ("%s[%s]%s [\033[91mErr\033[0m] Stop executing commands list on command  %s on device: %s:" % (bcolors.HEADER, nodename, bcolors.ENDC, command.get('command'), device_dict['ip']))
				logging.info ("Stop executing commands list on command  %s on device: %s:" % (command.get('command'), device_dict['ip']))
				break
			logging.info ("Command: %s on device: %s executed successfully" % (command.get('command'), device_dict['ip']))
			
			if command.get('cmd_type') == 'conf_set':
				print ("%s[%s]%s Command: \n%s\n on device: %s executed successfully" % (bcolors.HEADER, nodename, bcolors.ENDC, re.sub(',', '\n', command.get('command')), device_dict['ip']))
			else:
				print ("%s[%s]%s Command: %s on device: %s executed successfully" % (bcolors.HEADER, nodename, bcolors.ENDC, command.get('command'), device_dict['ip']))
		#add report logic, split search_type
		if len(command.get('search_type').split(',')) > 1:
			command['search_type'] = command.get('search_type').split(',')[0]
			command['last_val'] = 'last'
	
	queue[nodename] = commands
	logging.debug('\nEnd working whith node, result:\n{} '.format(pformat(queue)))
	try:
		if not fileno == None: os.close(fileno)
	except Exception as e:
		logging.debug('\nClose failed! {}'.format(e))	
	return queue
	
def conn_processes(function, devices, commands, cmd_exec_logic, max_process):
	'''
	Start multiprocessing for list of nodes
	!!! tested for cisco_ios!!!
		Arg:
			function: function that will be executed
			devices: list of nodes
			commands: list of commands
			cmd_exec_logic: logic of execution
			max_process: maximim number of parallel processes
	'''
	#using Pool whith control
	if len(devices) <= max_process: max_process = len(devices)
	print ('Count of parallel process: {}'.format(max_process))
	pool = multiprocessing.Pool(processes = max_process)
	#pool = multiprocessing.Semaphore(multiprocessing.cpu_count()) #this will detect the number of cores in your system and creates a semaphore with that  value. 
	#print ('cpu_count: {}'.format(multiprocessing.cpu_count()))
	results = [pool.apply_async(function, args=(device, commands, cmd_exec_logic, sys.stdin.fileno())) for device in devices]
	output = [p.get() for p in results]
	return output
	
