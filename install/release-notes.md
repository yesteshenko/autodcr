# Release Note

AutoDCR - automatization device configurations and reporting

Version: 0.2.7

## Introduction:

The document communicates the major new features and changes in this release of the AutoDCR.
It also documents known problems and workarounds.

## Compatible Products:

This product has been tested on the following platforms or with the following products:
    * Python 2.7.5 and 3.6
    * Cisco IOS, Cisco XR, Linux OS

## New Features:

* Added possibility use configuration templates for apply in device. Command will be executed in configurations mode.
  
  Use:
    Create configurations template and put in subdirectory data. 
    Set file name to parameter 'conf_template' in autodcr.conf or CLI, for example conf_template = conf_template_test.tpl
    If need, you can use variables in configurations template (not necessary).
        Format: 
            {var_name}
    Set variable to parameter 'conf_template_var' in autodcr.conf or CLI in json format
        Format:
            '{ "var_name": "var_value" [, "var_name": "var_value"] }'
        Buid-in variables:
            {nodename}     - will be set current nodename of device,
            {nodeip}       - will be set current ip of device

  Example
    configurations template:
    
        ```
        interface GigabitEthernet0/{if}
         description Test_script{num}
        exit
        ```
        
    CLI:
    
    ```./autodcr.py -commands commands_conf_template.csv -conf_template_var '{"if": "1", "num": "7"}'```


## Limitations:
    
* Feature tested only with Cisco IOS and Cisco XR
    
----

[Home](../README.md)