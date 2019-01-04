#!/usr/bin/env python

'''
 commands_gen.py

 Author:   Evgen Steshenko
 Year:     2018
 About:    Script prepare list of commands for executing on each node in list.
 
 General logic:
	Script replace all variables {num} in config_template from arguments of command line 'value' and create command.csv file for script 
	batch_cmd_exec  {num}: num equals number in the arguments line (starting from 0)
 
 Limitations:
    Only with Cisco IOS.
	 
 Example:
	{0} {1} 
	commands_gen.py one two
	{0} = one,  {1} = two
	
	Using:
 
 1. Check installation of Python (tested on Python 2.7.5 )
 2. Copy data in config_template file (same directory)
 3. Execute ./commands_gen.py
	usage: commands_gen.py [-h] [-logic logic] [-var value [value ...]]
                       [-prncnf print cnf]
					   
		optional arguments:
		  -h, --help            show this help message and exit
		  -logic logic          Set logic of executing command: sh_cmd - show command;
								cnf_cmd - line by line (with possibility of check on
								error and stop execution script; cnf_cmd_lst - by
								command list (set of command) (default = cnf_cmd_lst))

		  -var value [value ...]
								Set of values of variables than will be replaced in
								config_parrent
		  -prncnf print cnf     Print nativ configuration whith replaced all variables

'''

''' Initializing additional libs '''
import os, traceback, types, logging
import datetime, time
import re, csv
import operator
import argparse

''' Annanouncing global variables '''
paramname = ['cmdname','command','cmd_type','delay_factor','search','search_type','result_marker','expect']
line_cmdset = ['CnfCmdList','','conf_set','1','promt','count','','']
line_wm = ['WriteMem','write memory','general','1','OK','simple','Ok,Attention!','']
line_conft = ['EntConf','conf t','conf_enter','1','promt','count','','']
line_cnfcmd = ['cmd','','conf_cmd','1','promt','count','','']
line_cnfexit = ['ExitConf','exit','conf_exit','1','promt','count','','']
line_shcmd = ['cmd','','','1','promt','count','','']
cmd_list = []
cmd_set = []
debug = False

''' Parse script arguments '''
argparser = argparse.ArgumentParser(description='Script prepare list of commands for executing on each node in list')
argparser.add_argument("-logic", action="store", dest="logic", metavar='logic', choices=['cnf_cmd', 'cnf_cmd_lst', 'sh_cmd'], default='cnf_cmd_lst', required=False, help='Set logic of executing command:\n sh_cmd - show command;\n cnf_cmd - line by line (with possibility of check on error and stop execution script;\n cnf_cmd_lst - by command list (set of command)  (default = cnf_cmd_lst))')
#argparser.add_argument("var", metavar='value', nargs='+', help='Set of values of variables than will be replaced in config_template')
argparser.add_argument("-var", action="store", metavar='value', dest="var", required=False, nargs='+', help='Set of values of variables than will be replaced in config_template')
argparser.add_argument("-prncnf", action="store", dest="prncnf", metavar='print cnf', choices=['True', 'False'], default='False', required=False, help='Print nativ configuration with replaced all variables')

args = argparser.parse_args()
if debug: print('Arguments list:  %s' % (args))
in_filename = 'config_template'

''' Read and load templates '''
print ("Start working: %s" % (datetime.datetime.now()))
try:
	with open(in_filename) as open_file:
		alldata = open_file.read()
except IOError:
	print('[Err] Config template file: {} does not exist'.format(in_filename))
	exit(1)

if args.var != None: 
	try:
		lines_list = alldata.format(*args.var).split('\n')
	except IndexError:
		print ('[Err] Number of variables in arguments ({}) does not equals or less than variables in config_template'.format(len(args.var)))
		exit(2)
else:
	lines_list = alldata.split('\n')

if debug: print(lines_list)
 	
if args.prncnf == 'True':
	output_file_handle = open('config_replaced', "w")
	output_file_handle.write('\n'.join(lines_list))
	output_file_handle.close()
	#print '\n'.join(lines_list) #uncomment this if need configuration after replasing variables

for line in lines_list:
	search = re.findall('\!', line)
	if search: continue
	cmd_list.append(line.strip())
	
search = re.findall('conf.*t', lines_list[0])
if search: cmd_list = cmd_list[1:-2]

if args.logic == 'cnf_cmd':
	cmd_set.append(line_conft)
	for cmd	in cmd_list:
		cmd_set.append([re.sub(' ', '_', cmd),cmd,'conf_cmd','1','promt','count',''])
	cmd_set.append(line_cnfexit)
	cmd_set.append(line_wm)
if args.logic == 'cnf_cmd_lst':
	line_cmdset[paramname.index("command")] = ','.join(cmd_list)
	cmd_set.append(line_cmdset)
	cmd_set.append(line_wm)
if args.logic == 'sh_cmd':	
	for cmd	in cmd_list:
		cmd_set.append([re.sub(' ', '_', cmd),cmd,'','1','promt','count',''])
	
if debug: print cmd_set	

''' Write commands file '''
# File being opened in write mode
output_file_handle = open('commands.csv', "w") 
# write headers of variables to new file
output_file_handle.write(';'.join(str(e) for e in paramname)) 
for cmd	in cmd_set:
	output_file_handle.write('\n')
	output_file_handle.write(';'.join(str(e) for e in cmd)) 
# Close file handles
output_file_handle.close()
print ("End working")