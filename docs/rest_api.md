# RESTful API

## Introduction

The document describe rules and features for RESTful API. 
This is a simple application for easier to using AutoDCR in some cases.
!!! 
* Because RESTful API not use authorization and use HTTP use this only in secured LAN and for a short time (not as service or daemon)
!!!
----

## Configuration

In the configurations file autodcr.conf, section 'server', set next paramenerts:

1. enable server 
```server = True```
2. Set port
```port = 9090```
3. Set host
```host=0.0.0.0```

----

## Using

You can use Postman or any web browser.

----

## Available methods

1. [nodes](rest_api.md#nodes)
2. [cmd](rest_api.md#cmd)

----

## nodes

This GET method return node[s] parapeters if available. Using for checking correct node configurations.

### Parameters

- group	- group name of nodes from yaml data file
- name	- node name (or all) from yaml data file
- par	- parameners name for given node from yaml data file

### Example

```
http://192.168.1.7:9090/nodes?group=cisco_ios&name=all&par=cisco_ios_par

[
    {
        "username": "usr",
        "secret": "",
        "nodename": "node1",
        "device_type": "cisco_ios",
        "ip": "192.168.1.2",
        "password": "psw"
    },
    {
        "username": "usr",
        "secret": "",
        "nodename": "node2",
        "device_type": "cisco_ios",
        "ip": "192.168.1.3",
        "password": "psw"
    }
]
```

----

## cmd

This GET method executing commands for nodes and returns report.

### Parameters

- group				- group name of nodes from yaml data file
- name				- node name (or all) from yaml data file
- par				- parameners name for given node from yaml data file
- commands			- filename of commands list for executing (optional, default value getting from configurations file)
- conf_template		- configurations template (optional). Can be name of file: filename.tpl or directly commands template
- conf_template_var - variables for configurations template in json format (optional).
'						Format:
'							{ "var_name": "var_value" [, "var_name": "var_value"] }
'						Buid-in variables:
'							{nodename}     - will be set current nodename of device,
'							{nodeip}       - will be set current ip of device
						
### Example

```
http://192.168.1.7:9090/cmd?group=cisco_ios&name=node1&par=cisco_ios_par&commands=commands_conf_template.csv&conf_template=interface GigabitEthernet{if}\n description {descr}\nexit&conf_template_var={"if": "0/1", "descr": "Test_script"}


Summary report:

==========================================

   Node name: node1

------------------------------------------
| CmdName      | Result                    |
|:-------------|:--------------------------|
| Get versions | [ ME380x]                 |
| Config       | [search: prompt, count: 1] |
| WriteM       | Ok [ OK]                  |

==========================================
```

----


[Home](../README.md)