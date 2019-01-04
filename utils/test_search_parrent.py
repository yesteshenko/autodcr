#!/usr/bin/python

''' Initializing additional libs '''
import sys, os, traceback, types, logging
import datetime, time
import re, csv
import operator
#import ConfigParser
from ConfigParser import SafeConfigParser
from tabulate import tabulate
from pprint import pformat, pprint

''' Annanouncing global variables '''
delim = ''
print ('Script running on Python version: {}'.format(sys.version_info[0]))

''' Start user setting '''
#Load test data
test_data = open('test_output').read()

#Set regex parrent for testing
regex_parrent = '(Model number)(?:\s+:)( \S+)(?:\n)(System serial number)(?:\s+:) (\S+)'
#'Model number(?:\s+:) \S+(?:\n)System serial number(?:\s+:) \S+'
# for node sort search_type = 'complex' regex_parrent = 'Model number\s+: (?P<ModelNumber>\S+)\nSystem serial number\s+: (?P<SerialNumber>\S+)'
# for cmd sort 

#Set search type: simple|complex|count
search_type = 'simple'

''' End user setting '''

#Search
result = re.findall(regex_parrent, test_data)

#Search headers
header = re.findall('P<(\w+)>', regex_parrent)

'''

pprint(type(result[0]))
#Search negative
negative = re.findall('\?\!', regex_parrent)
if negative:
	newres = []
	for item in result:
		newres.append(item[0])
	result = newres
pprint(result)
'''	
''' Parse result '''
 
#len(result) >= 2
#logging.debug('\nSearch {} in output of cmd {} \n, result: {}\n'.format(regex_parrent, command_result.get('output'), ''.join(result)))
if len(result) > 0:
	#For debuging
	print ('\n Result of search:\n {}'.format(pformat(result)))
	print(type(result[0]))
	print ('\n Count of search result: {}'.format(len(result)))
	print ('\nParse output:\n')
	#For debuging
	if search_type == 'simple':
		if len(header) <= 1:
			if len(header) == 1: delim = ':'
			if len(result) == 1 and isinstance(result[0], tuple):
				print ('Result [{}{} {}]'.format(''.join(header), delim, ' '.join(result[0])))
			elif isinstance(result[0], list) == False and isinstance(result[0], tuple) == False:
				print ('Result [{}{} {}]'.format(''.join(header), delim, ','.join(result)))
			else:		
				search_type = 'complex'
		else:		
			search_type = 'complex'
		'''
		if len(header) <= 1 and search_type != 'complex':
			print ( 'Successful [{}: {}]'.format(':'.join(header), ','.join(result)))
		elif search_type != 'complex':
			print ( 'Successful [search: {}; result: {}]'.format(regex_parrent, ','.join(result)))#type(result)(x.encode('ascii') for x in result))
		'''
	if search_type == 'complex':
		#result_header = ['Coll'] * (len(result))
		result_list = []
		if sys.version_info[0] == 2: 
			if isinstance(result[0], basestring):# or isinstance(result[0], unicode): #'unicode for list or tuple tabulate work well'
				result_list.append(result)
				result = result_list
		if sys.version_info[0] == 3:
			if isinstance(result[0], str): # or isinstance(result[0], unicode) 'unicode for list or tuple tabulate work well'
				result_list.append(result)
				result = result_list
		print ( 'Successful [complex search, result:\n {}]'.format(tabulate(result, headers=header, tablefmt='grid')))	
	
	elif not search_type == 'simple':
		if len(header) == 1 :
			print ( 'Successful [{}: {}]'.format(''.join(header), len(result)))
		else:
			print ( 'Successful [search: {}, count: {}]'.format(regex_parrent, len(result)))	
	
else:
	print ('Fail find search value')