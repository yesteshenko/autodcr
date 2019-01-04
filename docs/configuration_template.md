# Configuration template

  The document describe rules for create configuration template for apply in device. Command will be executed in configurations mode. 
Example can found in directory 'data'.
It also documents examples.

---

**Use**:

* Create configurations template and put in subdirectory data.
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
     description Test_script{num}
    exit
```

CLI:

```./autodcr.py -commands commands_conf_template.csv -conf_template_var '{"if": "1", "num": "7"}'```

----

[Home](../README.md)