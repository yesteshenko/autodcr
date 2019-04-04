from flask import Flask, make_response
from flask_restful import Api, Resource, reqparse
import yaml, logging, os, re
from pprint import pformat, pprint
from lib.ssh_client import *
from lib.utils import *

def parcerest_conf_template(args, commands_list):
	''' 
	Read and parce configuration template
		Arg:
			commands_list: list of commands
			args: REST arguments  
	'''
	for cmd_index, command in enumerate(commands_list):
		if re.match('Config', command[0]) != None: 
			commands_list[cmd_index][1] = re.sub('\n', ',', args.get('conf_template'))
			break

	if args.get('conf_template_var'):
		dict_var = json.loads(args.get('conf_template_var'))
		for cmd_index, command in enumerate(commands_list):
			search = re.match('Config', command[0])
			if re.match('Config', command[0]) != None:
				for var in dict_var:
					commands_list[cmd_index][1] = re.sub('\{'+var+'\}', dict_var.get(var), command[1])
				break
	return commands_list
	
def server(BASE_DIR, nodes_file, programargs, cmd_exec_logic, max_process, server_par):
	''' 
	RESTful API server
		Arg:
			BASE_DIR: base directory of script
			nodes_file: file whith list of nodes
			commands_list: list of commands
			programargs: main program command arguments
			cmd_exec_logic: logic of execution
			max_process: maximim number of parallel processes
			server_par: parameters for server
	'''
	app = Flask('autodcr')
	api = Api(app)
	
	class Nodes(Resource):
		def get(self, **kwargs):
			# Define parser and request args
			parser = reqparse.RequestParser()
			parser.add_argument('group', type=str)
			parser.add_argument('name', type=str)
			parser.add_argument('par', type=str)
			args = parser.parse_args()
			'''example'''
			# http://172.17.100.7:9090/nodes?group=cisco_ios&name=all&par=cisco_ios_par 
			# pprint(args) -> {'group': 'cisco_ios', 'name': 'all', 'par': 'cisco_ios_par'}
			'''Get nodes config'''
			nodes_data = get_data_yaml(nodes_file, [args['group'], args['name'], args['par']])
			nodes_list_dist = nodes_data.get('dict')
			nodes_list = nodes_data.get('list')
			logging.debug('%s:\n  %s' % ('Server, get nodes', pformat(nodes_list_dist)))
			if nodes_list_dist:
				return nodes_list_dist, 200
			return "Node[s] not found", 404

	class Cmd(Resource):
		def get(self, **kwargs):
			results = []						
			# Define parser and request args
			parser = reqparse.RequestParser()
			parser.add_argument('group', type=str)
			parser.add_argument('name', type=str)
			parser.add_argument('par', type=str)
			parser.add_argument('commands', type=str)
			parser.add_argument('conf_template', type=str)
			parser.add_argument('conf_template_var', type=str)
			args = parser.parse_args()
			'''example'''
			#http://172.17.100.7:9090/cmd?group=cisco_ios&name=HM_N_PE_L&par=cisco_ios_par&commands=commands_conf_template.csv&conf_template=interface GigabitEthernet{if}\n description {descr}\nexit&conf_template_var={"if": "0/1", "descr": "Test_script"}
			'''Get nodes config'''
			nodes_data = get_data_yaml(nodes_file, [args['group'], args['name'], args['par']])
			nodes_list_dist = nodes_data.get('dict')
			nodes_list = nodes_data.get('list')
			'''Get commands config'''
			commands_list = get_data(os.path.normpath(BASE_DIR + 'data/' + programargs.commands_filename), 'commands')
			if args.get('commands') != None:
				commands_list = get_data(os.path.normpath(BASE_DIR + 'data/' + args.get('commands')), 'commands')
			if args.get('conf_template') != None:
				if re.search('\.tpl', args.get('conf_template')) != None:
					if args.get('conf_template_var') != None: programargs.conf_template_var = args.get('conf_template_var')
					commands_list = parce_conf_template(os.path.normpath(BASE_DIR + 'data/' + args.get('conf_template')), commands_list, programargs)
				else:
					commands_list = parcerest_conf_template(args, commands_list)
			#Transformation list to dictionary
			commands_list_dist = lits_to_dict(commands_list)
			''' Executing commands '''
			if cmd_exec_logic.get('multiprocessing_exec'):
				results =  conn_processes(connect_ssh, nodes_list_dist, commands_list_dist, cmd_exec_logic, max_process)
			else:
				for device in nodes_list_dist:
					results.append(connect_ssh(device, commands_list_dist, cmd_exec_logic))
			logging.debug('Result of exec cmd on nodes: %s' % (pformat(results)))
			''' Reporting '''
			print_full_report_to_file(results, BASE_DIR)
			summary_report = prepare_summary_report(results, BASE_DIR, programargs.sort, nodes_list[1:], commands_list[1:])
			if summary_report:
				headers = {'Content-Type': 'text/html'}
				return make_response(summary_report,200,headers)
			return "Command[s] not executed", 404		
		
	api.add_resource(Nodes, "/nodes")	
	api.add_resource(Cmd, "/cmd")	
	app.run(debug=server_par['logstatus'], host=server_par['host'], port=server_par['port'])