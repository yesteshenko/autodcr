''' Initializing additional libs '''
import multiprocessing
from netmiko import ConnectHandler
import logging, re
from lib.utils import check_output
from pprint import pformat, pprint
import subprocess as sp
from tabulate import tabulate

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
		search = re.match('Error exec cmd ', result)
		if search != None: 
			logging.debug('Found error on executing command:\n%s' % (pformat(result)))
			print ('Found error on executing command:\n%s' % (result))
			return True
	if cmd_exec_logic.get('cmd_exec_seachfail_logic'):
		search = re.match('Fail find search value', result)
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
		print "catch: {}".format(command.get('expect'))
		return command.get('expect')
	if device_type == 'cisco_ios' or device_type == 'cisco_xr' or device_type == 'cisco_xe':
		if command.get('search') == 'promt': return current_prompt #'.*#$'
		if command.get('search') == 'request': return '.*: $'
		if command.get('search') == 'confirm': return '.* \[.*\]'
		return '.*#$'
	#if device_type == 'linux': return '# $'
	if command.get('search') == 'promt': return current_prompt
	return ''
	# .* (not always work correctly) <= no matter what get, or restrict expect value =>  '.*#($|\s+)'
	
def connect_ssh(device_dict, commands, cmd_exec_logic):
	'''
	Connect to device and execute command list
	!!! tested for cisco_ios!!!
		Arg:
			devices: parameters of device (dict)
			queue: list of result
			commands: list of commands
			cmd_exec_logic: logic of execution
	'''
	queue = {}
	nodename = device_dict.get('nodename')
	del(device_dict['nodename'])
	print ("Connection to device %s" % device_dict['ip'])
	logging.info("Connection to device %s" % device_dict['ip'])
	try:
		ssh = ConnectHandler(**device_dict)
	except Exception as e:
		logging.debug('\nConnect failed! {}'.format(e))
		print('\nConnect failed! {}'.format(e))
		logging.info ("Stop executing commands")
		print('\nStop executing commands')
		failed_dic = [{'cmdname': 'Err', 'output': e, 'search': '' }]
		queue[nodename] = failed_dic
		return queue
	ssh.enable()
	for cmd_index, command in enumerate(commands):
		#Checking command
		if command.get('command') == None: 
			logging.debug('\nSomething wrong in command syntax\'s! Incoming config for current command:\n{} '.format(pformat(command.get('command'))))
			print('\nSomething wrong in command syntax\'s! Incoming config for current command:\n{} '.format(pformat(command.get('command'))))
			logging.info ("Stop executing commands")
			print('\nStop executing commands')
			failed_dic = [{'cmdname': 'Err', 'output': 'Something wrong in command syntax', 'search': '' }]
			queue[nodename] = failed_dic
			return queue			
		cmd=''
		cmd_list = []
		cmd_var_search = []
		cmd_var_search = re.findall('\{\}', command.get('command'))
		command['command'] = re.sub('\{nodename\}', nodename, command.get('command'))
		command['command'] = re.sub('\{nodeip\}', device_dict['ip'], command.get('command'))
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
						#commands[cmd_index]['cmdname'] = commands[cmd_index].get('cmdname') + '(' + str(var_index) + ')'
					else:
						cmd_dic = {}
						cmd_dic = command.copy()
						cmd_dic['command'] = cmd
						cmd_dic['cmdname'] = cmd_dic.get('cmdname') + '(' + str(var_index) + ')'
						commands.insert(cmd_index + var_index, cmd_dic)
				logging.debug('\nNew command list:\n' + pformat(commands))
			else:
				logging.info ("Stop executing commands")
				print ("Stop executing commands list on command  %s on device: %s:" % (command.get('command'), device_dict['ip']))
				logging.info ("Stop executing commands list on command  %s on device: %s:" % (command.get('command'), device_dict['ip']))
				break
		print ("Try to execute command: %s on device: %s:" % (command.get('command'), device_dict['ip']))
		logging.info ("Try to execute command: %s on device: %s:" % (command.get('command'), device_dict['ip']))

		cmd = command.get('command')
		if command.get('command') == 'enter': cmd = '\n'
		if command.get('cmd_type') == 'conf_enter': 
			command['output']  =  ssh.config_mode()
		elif command.get('cmd_type') == 'conf_exit': 
			command['output']  =  ssh.exit_config_mode()
		elif command.get('cmd_type') == 'conf_set':
			cmd_list = command.get('command').split(',')
			command['output']  =  ssh.send_config_set(cmd_list, strip_prompt = False, strip_command = False, delay_factor = int(command.get('delay_factor')))#.encode('ascii').decode('utf-8')
		elif command.get('cmd_type') == 'os_exec':
			cmd = re.sub('\<\>', check_output(commands[cmd_index-1]), command.get('command'))
			#result = re.findall(commands[cmd_index-1].get('search'), commands[cmd_index-1].get('output'))
			#cmd = re.sub('\<\>', tabulate(result, headers=re.findall('P<(\w+)>', commands[cmd_index-1].get('search')), tablefmt='html'), command.get('command'))
			cmd = re.sub('\{command\}', commands[cmd_index-1].get('command'), cmd)
			cmd = re.sub('\{nodename\}', nodename, cmd)
			cmd = re.sub('\{ip\}', device_dict['ip'], cmd)
			cmd = re.sub('\n', '\n\r', cmd)
			print (cmd)
			command['output']  =  sp.check_output(cmd, shell=True)
		else:
			logging.debug('Current promt is %s' % (ssh.find_prompt()))
			#print (ssh.find_prompt())
			expect_promt =  get_expect_string(command, ssh.find_prompt(), device_dict['device_type'])
			if expect_promt == "":
				command['output']  =  ssh.send_command(cmd, strip_prompt = False, strip_command = False, delay_factor = int(command.get('delay_factor')))#.
			command['output']  =  ssh.send_command(cmd, strip_prompt = False, strip_command = False, delay_factor = int(command.get('delay_factor')), expect_string = expect_promt)#.encode('ascii').decode('utf-8')
		logging.info("Checking executing commands logic:")
		if cmd_exec_logic.get('cmd_exec_err_logic') or cmd_exec_logic.get('cmd_exec_searchfail_logic'):
			result = chech_fail_exec(command, cmd_exec_logic)
			if result: 
				logging.info ("Stop executing commands")
				print ("Stop executing commands list on command  %s on device: %s:" % (command.get('command'), device_dict['ip']))
				logging.info ("Stop executing commands list on command  %s on device: %s:" % (command.get('command'), device_dict['ip']))
				break
			logging.info ("Command: %s on device: %s executed successfully" % (command.get('command'), device_dict['ip']))
			print ("Command: %s on device: %s executed successfully" % (command.get('command'), device_dict['ip']))
		#add report logic, split search_type
		if len(command.get('search_type').split(',')) > 1:
			command['search_type'] = command.get('search_type').split(',')[0]
			command['last_val'] = 'last'
	
	queue[nodename] = commands
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
	pool = multiprocessing.Pool(processes = max_process)
	#pool = multiprocessing.Semaphore(multiprocessing.cpu_count()) #this will detect the number of cores in your system and creates a semaphore with that  value. 
	#print ('cpu_count: {}'.format(multiprocessing.cpu_count()))
	results = [pool.apply_async(function, args=(device, commands, cmd_exec_logic)) for device in devices]
	output = [p.get() for p in results]
	return output
	
