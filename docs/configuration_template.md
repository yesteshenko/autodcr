# Configuration template

  The document describe rules for create configuration template for apply in device. Command will be executed in configurations mode. 
Example can found in directory 'data'.
It also documents examples.

---

## 1 Use argument list of CLI

**Use**:

* Create configurations template and put in subdirectory' data'.
* Set file name to parameter 'conf_template' in autodcr.conf or CLI, for example conf_template = conf_template_test.tpl
* If need, you can use variables in configurations template (not necessary).

***Format***:

{var_name}

Set variable to parameter 'conf_template_var' in autodcr.conf or CLI in json format

***Format***:

'{ "var_name": "var_value" [, "var_name": "var_value"] }'

***Buid-in variables***:

{nodename}     - will be set current nodename of device,  
{nodeip}     - will be set current ip of device

  ***Example***:
  
configurations template:

```
    interface GigabitEthernet0/{if}
     description {descr}
    exit
```

cmds:

```Config;;conf_tpl;1;prompt;;```

CLI:

```./autodcr.py -commands commands_conf_template.csv -conf_template_var '{"if": "1", "descr": "Test_script"}'```

## 2 Use command

!This use case has higher priority than using CLI

**Use**:

* Create configurations template and put in subdirectory 'data'.
* If need, you can create file with set of variables file for each node and put in subdirectory 'data' (not necessary).
* Set command in command file

***Format***:

Configurations template use same logic, that described above.

Variables file:

* Used csv file format
* First line contains variables name what will be used for replece in configurations template;
* next lines contains value of each variable;
* parameters separator is - ';'.

  ***Example***:
  
```  
nodename;if;descr
Node_L;1;Left
Node_R;1;Right
```

cmds:

```Config;template_filename.tpl,var_filename_.csv;conf_tpl;1;prompt;;```

For this example will be replaced variable {if} and {descr} for each of nodes 'Node_L and Node_R' when will be connected to them

```Config;template_filename.tpl,var_filename_.csv,Node_L;conf_tpl;1;prompt;;```

For this example will be replaced variable {if} and {descr} using set of variables for 'Node_L' (connected nodename will not be used)

----

[Home](../README.md)