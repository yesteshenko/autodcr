# User guide 

## Introduction

### 1.1. test
The document describe rules and features for AutoDCR

---
## Directory structure


autodcr/

	conf            - includes initial configuration     
	data            - includes settings for scripts (commands, nodes, templates ...)
	docs            - includes documentation
	examples        - includes some examples
	install         - includes documentation of installation
	lib             - includes libraries  
	log             - includes log
	report          - includes reports
	utils           - includes additional tools that help prepare and test configurations
	autodcr.py      - automatization device configurations and reporting script
	LICENSE         - license copy
	README.md       - start page of documentations

---

## Static configurations

Starting static configurations locate in file [autodcr.conf]
Description configurations parameters can be found in that file and below

---

## Dynamic configurations

For dynamic configurations, use CLI

	optional arguments:
	-h, --help                show this help message and exit
	--version                 show program's version number and exit
	-nodes filename           list of nodes with connections parameters 
					(default value getting from configurations file)
	-nodes_type type          type of config file for import nodes: for CSV format - csv, for YAML format - yaml 
					(default value getting from configurations file)
	-nodes_set val val val    Set of values of nodes from yaml data file. Arguments:
					1st: group, 
					2nd: node_name or all, 
					3rd: parameners
	-commands filename        list of commands for executing (default value getting from configurations file)
	-conf_template filename   configurations template (default value getting from configurations file)
	-conf_template_var json   variables for configurations template in json format: 'json' 
					(default value getting from configurations file )
	-processing type          logic of processing nodes: 
					multiprocessing = True, 
					singlrocessing (exec in queue) = False 
					(default value getting from configurations file)
	-error type               executing commands logic when error (fail) found: 
					stop execution commands = True, 
					continue execution command = False 
					(default value getting from configurations file)
	-searchfail type          executing commands logic when fail search value of output: 
					stop execution commands = True, 
					continue execution commands = False 
					(default value getting from configurations file)
	-sort type                Sort by node = node, sort by command = command 
					(default value getting from configurations file)
	-export type              Set export result. Values: 
					False - no export; 
					excel - export result of search to excel (only command in search type mode: complex); 
					word - export output of command execution to word template (./data/protocol_template.docx) 
					(default value getting from configurations file)

	---

## Usage

For using script, you need perform the following actions:
1. set startup configurations, see file [autodcr.conf]

1.1. [test](userguide.md###1.1.)

2. prepare configuration of device, see [Nodes]
3. prepare commands list, see [Commands]
4. prepare commands template (optional), see [template]
5. prepare Doc template for report (optional), see [protocol template]
6. start script: 
```
autodcr.py [-h] [--version] [-nodes filename] [-nodes_type type]
                    [-nodes_set val val val] [-commands filename]
                    [-conf_template filename] [-conf_template_var json]
                    [-processing type] [-error type] [-searchfail type]
                    [-sort type] [-export type]
```



---

[Home](../README.md)

[autodcr.conf]: ../conf/autodcr.conf
[Nodes]: nodes.md#Nodes
[Commands]: commands.md
[template]: configuration_template.md
[protocol template]: protocol_template.md

