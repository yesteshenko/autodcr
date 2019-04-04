# Use cases 

## Introduction

The document describe examples and use cases for AutoDCR

===

## Use cases

**Table of Contents**

1. [Search][1]
1.1. [Search MAC address][11]
1.2. [cdp neighbors discovery][12]
1.3. [Version and serial number discovery][13]
1.4. [Ping with sort mode command][14]
1.5. [Check port status][15]
1.6. [Check predefined status][16]
1.7. [Check protocol and use result marker][17]

2. [Log parsing][2]
2.1. [Log parsing (flapping)][21]
2.2. [Log parsing (select last message)][22]

3. [Use search as value][3]
3.1. [Command chain (simple)][31]
3.2. [Command chain (complex)][32]
3.3. [Send result of execution previous command to shell OS command][33]

4. [Build-in command and variables][4]
4.1. [Use timeout for execution commands][41]
4.2. [Use build-in variables (backup)][42]
4.3. [SSH connections through device to another device][43]

5. [Configuration device][5]
5.1. [Configuration device in mode 'list of commands'][51]
5.2. [Configuration device in mode 'command by command'][52]
5.3. [Configuration device in mode 'basic configuration template'][53]
5.4. [Configuration device in mode 'configuration template per command'][54]
5.5. [Configuration device in mode 'configuration template per command with table of variables'][55]
5.6. [Configuration device in mode 'configuration template per command with table of variables  and nodename'][56]

6. [Request user for search value][6]
6.1. [Request user for search value][61]
6.2. [Request user for set of variables][62]

7. [RestAPI][7]
7.1. [Get nodes][71]
7.2. [Get cmd][72]

8. [Export result][8]
8.1. [Export result of command execution to excel][81]
8.2. [Export result of command execution to word][82]

===

### 1. Search

#### 1.1. Search MAC address

For this example we search MAC address

commands file:
```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker
Get MAC;show arp;;;\S+\s+(?P<IPaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+\S+\s+(?P<MAC>[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\.[0-9a-fA-F]{4})\s+\S+\s+(?P<Interface>.*);complex;Ok,Err;
```

Output:

```
Successful [complex search, result:
 +--------------+----------------+-------------+
| IPaddress    | MAC            | Interface   |
+==============+================+=============+
| 192.168.1.3 | 04da.d2d5.1bc0 | Vlan606     |
+--------------+----------------+-------------+
| 192.168.1.2 | 04da.d2d4.bfc0 | Vlan4001    |
+--------------+----------------+-------------+]
```

[Use cases]
---

#### 1.2. cdp neighbors discovery

For this example we search cdp neighbors

commands file:
```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker
Get cdp neighbors;show cdp neighbors detail;;;Device ID: (?P<DeviceID>.*)\n.*\n  IP address: (?P<IPaddress>.*)\nPlatform: (?P<Platform>.*),.*\nInterface: (?P<Local>.*),.*\(outgoing port\): (?P<Outgoing>.*);complex;Ok,Err;
```

Output:

```
Successful [complex search, result:
 +---------------------+-------------+-----------------------+---------------------+---------------------+
| DeviceID   | IPaddress   | Platform              | Local               | Outgoing            |
+=====================+=============+=======================+=====================+=====================+
| router_1   | 192.168.1.2  | cisco ME-3800X-24FS-M | GigabitEthernet0/10 | GigabitEthernet0/10 |
+---------------------+-------------+-----------------------+---------------------+---------------------+
| router_2   | 192.168.1.3  | cisco ME-3800X-24FS-M | GigabitEthernet0/23 | GigabitEthernet0/23 |
+---------------------+-------------+-----------------------+---------------------+---------------------+]
```

[Use cases]
---

#### 1.3. Version and serial number discovery

For this example we search cdp version and serial number

commands file:
```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker
Get versions;sh ver;;1;(?P<Inventory>Model number)(?:\s+:)( \S+)(?:\n)(System serial number)(?:\s+:) (\S+);simple;
```

Output:

```
| nodename   | Result                                                                      |
|:-----------|:----------------------------------------------------------------------------|
| router_1   | [Inventory: Model number  ME-3800X-24FS-M System serial number FOC1645X1E3] |
```

[Use cases]
---

#### 1.4. Ping with sort mode command

For this example we search result of ping.
In CLI used mode -sort command

CLI:

```
./autodcr.py -nodes_type csv -nodes nodes_test.csv -commands /examples/commands_ping.csv -sort command
```

commands file:
```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker
ping;ping ip 192.168.1.1;;1;Success rate is (?P<Result>\d{2,3});simple;Ok,Error!
```

Output:

```
==========================================

   Commands name: ping

------------------------------------------
| nodename   | Result         |
|:-----------|:---------------|
| router_1  | Ok [Result: 100] |
| router_2  | Ok [Result: 100] |

==========================================
```

[Use cases]
---

#### 1.5. Check port status

For this example we search status of voice port.

CLI:

```
./autodcr.py -nodes_type csv -nodes nodes_test.csv -commands /examples/commands_voiceport.csv
```

commands file:
```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker
Get voice port;show voice port;1;(ISDN \d\/\d).*\n.*\n (Operation State is \S+)\n (Administrative State is \S+)+;complex;
```

Output:

```
------------------------------------------
| CmdName        | Result|
|:---------------|:--------------------------------------------------|
| Get voice port | [result:
                         command:show voice port
                         +----------+----------------------------+----------------------------+
                        | ISDN 3/0 | Operation State is DORMANT | Administrative State is UP |
                        +----------+----------------------------+----------------------------+
                        | ISDN 3/1 | Operation State is DORMANT | Administrative State is UP |
                        +----------+----------------------------+----------------------------+] |
```

[Use cases]
---

#### 1.6. Check predefined status

For this example we search status of l2vpn that is UP.

commands file:
```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker
l2vpn status;Sho l2vpn atom vc;;1;(?P<Service>pw.*)(?P<Status>UP);complex;Ok, Err !
```

Output:

```
------------------------------------------
| CmdName      | Result|
|:-------------|:--------------------------------------------------|
| l2vpn status | Ok [result:
                         command:Sho l2vpn atom vc
                         +----------------------------------------------------------------------+----------+
                        | Service| Status     |
                        +======================================================================+==========+
                        | pw44102   192.168.1.1        44         p2p    lab                  | UP       |
                        +----------------------------------------------------------------------+----------+
```

[Use cases]
---

#### 1.7. Check protocol and use result marker

For this example we search status of BGP Neighbor that is not UP and mark in report 'Error' if search is successful.
This mean negative search result it is ok for us.

commands file:
```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker
BGP sum;sho ip bgp ipv4 uni sum;general;1;Active|Idle;simple;Error!,Ok;
```

Output:

```
------------------------------------------
| CmdName     | Result|
|:------------|:--------------------------------------------------|
| BGP sum     | Ok (Fail find search value)|
```

[Use cases]
---

### 2. Log parsing

#### 2.1. Log parsing (flapping)

For this example we search last appearance flapping message in log.

commands file:
```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker
Log flapping;sh log | inc flapping ;;1;(?P<Date>\w{3} \d{2} \d{2}:\d{2}:\d{2}.\d{3}:).*Host (?P<MacAddr>\S+) in vlan (?P<Vlan>\d+) is flapping between port (?P<Port1>\S+) and port (?P<Port2>\S+);simple,last;Ok,Error!;
```

LOG:

```
Oct 3 12:49:15.941: %SW_MATM-4-MACFLAP_NOTIF: Host f04d.a206.7fd6 in vlan 1 is flapping between port Gi0/5 and port Gi0/16
Oct 3 12:49:15.941: %SW_MATM-4-MACFLAP_NOTIF: Host f04d.a206.7fd8 in vlan 1 is flapping between port Gi0/8 and port Gi0/18
```

Output:

```
------------------------------------------
| CmdName      | Result|
|:-------------|:--------------------------------------------------|
| Log flapping | Error! [result:
					command:sh log | inc flapping
					 +----------------+--------+---------+---------+
					| MacAddr        |   Vlan | Port1   | Port2   |
					+================+========+=========+=========+
					| f04d.a206.7fd6 |      1 | Gi0/5   | Gi0/16  |
					+----------------+--------+---------+---------+
					| f04d.a206.7fd8 |      1 | Gi0/8   | Gi0/18  |
					+----------------+--------+---------+---------+]
```

[Use cases]
---

#### 2.2. Log parsing (select last message) 

For this example we search last appearance event state DOWN for MPLS peer in line report style (for command sort type).

commands file:
```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker
Log;sh log | inc vcid 44;;1;\*(?P<LastEvent>\S+ \d{2} \d{2}:\d{2}:\d{2}.\d{3}:)(?:.*)( vcid 44)(?:.*)( state DOWN);simple,last;Ok,Error!;
```

LOG:

```
*Nov 22 08:31:48.717: %XCONNECT-5-PW_STATUS: MPLS peer 192.168.1.99 vcid 44, VC state DOWN, PW Err
*Nov 22 08:31:49.737: %XCONNECT-5-PW_STATUS: MPLS peer 192.168.1.99 vcid 44, VC state UP
```

Output:

```
   Commands name: Log

------------------------------------------
| nodename   | Result                                                 |
|:-----------|:-------------------------------------------------------|
| router_1   | [LastEvent: Nov 22 12:00:22.973:, vcid 44, state DOWN] |
```

[Use cases]
---

### 3. Use search as value

#### 3.1. Command chain (simple)

For this example we search l2vpn state 'DOWN' and each found 'vcid' send to next command.

commands file:

```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker
l2vpn status;Sho l2vpn atom vc;;1;\S+\s+\S+\s+(?P<vcid>\d+)\s+\S+\s+\S+\s+DOWN;simple;Attention!,Ok
l2vpn status detail;Sho l2vpn atom vc vcid {} detail;;1;(?P<Line>.*)(?P<Status>DOWN);complex;Attention!,Ok
```

Output:

```
------------------------------------------
| CmdName                 | Result|
|:------------------------|:--------------------------------------------------|
| l2vpn status            | Err ! [vcid: 300512 300518 ]|
| l2vpn status detail     | Err ! [result:
                         command:Sho l2vpn atom vc vcid 300512 detail
                         +-------------------------------------------+----------+
                        | Line                                      | Status   |
                        +===========================================+==========+
                        | Status received from access circuit     : | DOWN     |
                        +-------------------------------------------+----------+
                        | Status sent to network peer             : | DOWN     |
                        +-------------------------------------------+----------+]|
| l2vpn status detail(1)  | Err ! [result:
                         command:Sho l2vpn atom vc vcid 300518 detail
                         +-------------------------------------------+----------+
                        | Line                                      | Status   |
                        +===========================================+==========+
                        | Status received from access circuit     : | DOWN     |
                        +-------------------------------------------+----------+
                        | Status sent to network peer             : | DOWN     |
                        +-------------------------------------------+----------+]|
```

[Use cases]
---

#### 3.2. Command chain (complex)

For this example we search l2vpn state 'DOWN' and each found 'vcid' send to next command.
This example use report of execution previous command as variable set for use in next command.
Can be used not only one variables and command will be executed as many time as will be lines in table of variables. 

commands file:

```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker
l2vpn status;Sho l2vpn atom vc;;1;(?P<If>\S+)\s+(?P<PeerID>\S+)\s+(?P<vcid>\d+)\s+\S+\s+(?P<Name>l3vpn\S+)\s+DOWN;complex; Err !,Ok
l2vpn status detail;Sho l2vpn atom vc vcid {$vcid} detail;;1;(?P<Line>.*)(?P<Status>DOWN);complex; Err !,Ok
```

Output:

```
------------------------------------------
| CmdName                | Result|
|:-----------------------|:--------------------------------------------------|
| l2vpn status           | Err ! [result:
                         command:Sho l2vpn atom vc
                         +----------+----------+--------+--------------------------+
                        | If       | PeerID   |   vcid | Name                     |
                        +==========+==========+========+==========================+
                        | pw100034 | 192.168.1.9 | 300511 | l3vpn_TestService_3047_9 |
                        +----------+----------+--------+--------------------------+
                        | pw100035 | 192.168.1.9 | 300512 | l3vpn_TestService_3048_9 |
                        +----------+----------+--------+--------------------------+] |
| l2vpn status detail    | Err ! [result:
                         command:Sho l2vpn atom vc vcid 300511 detail
                         +-------------------------------------------+----------+
                        | Line                                      | Status   |
                        +===========================================+==========+
                        | Status received from access circuit     : | DOWN     |
                        +-------------------------------------------+----------+
                        | Status sent to network peer             : | DOWN     |
                        +-------------------------------------------+----------+]|
| l2vpn status detail(2) | Err ! [result:
                         command:Sho l2vpn atom vc vcid 300512 detail
                         +-------------------------------------------+----------+
                        | Line                                      | Status   |
                        +===========================================+==========+
                        | Status received from access circuit     : | DOWN     |
                        +-------------------------------------------+----------+
                        | Status sent to network peer             : | DOWN     |
                        +-------------------------------------------+----------+]|

```

[Use cases]
---

#### 3.3. Send result of execution previous command to shell OS command

For this example we search version of IOS and send to next command where will be execuded shell OS command. 

In this examle of shell OS command we will send report to email, but you can for example send some output or configurations to external script for prepare new config that will be used in next command. 

Also this is used build-in variables {nodename} - current node name and {command} - previous command

commands file:
```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker
Get versions;sh ver;;;Cisco IOS Software, (?P<version>\w+);TextFSM;
OSexec;(echo -e "Result of executing {command} on {nodename}:\n<>" | sendEmail -f [sendEmail parameters] -u "AutoDCR" -m);os_exec;;Email was sent successfully!;simple;
```

[Use cases]
---

### 4. Build-in command and variables

#### 4.1. Use timeout for execution commands.

For this example we set some time out before ping.

This is may be useful if you before do some configuration with protocol or routing.

commands file:

```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker
Waite5s;timeout;;5;;;;
ping;ping ip 192.168.1.1;;1;(?P<ipaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*\n.*\nSuccess rate is (?P<rate>\d{1,3});complex;Ok,Error!
```

[Use cases]
---

#### 4.2. Use build-in variables (backup)

For this example we do backup config to flash and than copy to ftp.
For that used build-in variables {nodename} - current node name and {date} - current date
Also this shows how to confirm command if it needed.

commands file:

```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker;expect
Backup;copy running-config flash:{nodename}_backup_{date};;1;.*\[(?P<file>[a-zA-Z_0-9]*)\]\?;simple;Ok,Error!;.*[.*]?
BackupConfirm;enter;;1;.*bytes copied;simple;Ok,Error!;
CopyBackup;copy flash:{nodename}_backup_{date} ftp://192.168.1.3;;1;Address or name.*;simple;Ok,Error!;.*[.*]?
CopyBackupConfirm;enter;;1;Destination filename.*;simple;Ok,Error!;.*[.*]?
CopyBackupConfirm;enter;;1;.*bytes copied;simple;Ok,Error!;.*#
```

Output:

```
------------------------------------------
| CmdName           | Result|
|:------------------|:--------------------------------------------------|
| SaveRunCnfToLog   | Ok [ router_1#]                                         |
| Backup            | Ok [file: router_1_backup_20190314]                     |
| BackupConfirm     | Ok [ 25024 bytes copied]                                 |
| CopyBackup        | Ok [ Address or name of remote host [192.168.1.3]? ]  |
| CopyBackupConfirm | Ok [ Destination filename [router_1_backup_20190314]? ] |
| CopyBackupConfirm | Ok [ 25024 bytes copied]                                 |

```

[Use cases]
---

#### 4.3. SSH connections through device to another device

For this example we do: 
- SSH connections through device to another device;
- ping;
- check current prompt;
- exit from ssh session;
- check current prompt.

commands file:

```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker;expect
Connect;ssh 192.168.1.101;conf_cmd;1;request;simple;Ok,Error!;Password:
EntPassw;cisco;;1;.*#$;simple;Ok,Error!;.*#$
ping;ping ip 192.168.1.1;;1;(?P<ipaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*\n.*\nSuccess rate is (?P<rate>\d{1,3});complex;Ok,Error!
GetPrompt;enter;;1;.*#$;simple;Ok,Error!;.*#$
SSH_Exit;exit;;1;.Connection.*closed;simple;Ok,Error!;.*#$
GetPrompt;enter;;1;.*#$;simple;Ok,Error!;.*#$
```

Output:

```
------------------------------------------
| CmdName   | Result|
|:----------|:--------------------------------------------------|
| Connect   | Ok [ Password: ]|
| EntPassw  | Ok [ router_2#]|
| ping      | Ok [result:
			 command:ping ip 192.168.1.1
			 +---------------+--------+
			| ipaddress     |   rate |
			+===============+========+
			| 192.168.1.1   |    100 |
			+---------------+--------+] |
| GetPrompt | Ok [ router_2#]|
| SSH_Exit  | Ok [ [Connection to 192.168.1.101 closed]|
| GetPrompt | Ok [ router_1#]|
```

[Use cases]
---

### 5. Configuration device

#### 5.1. Configuration device in mode 'list of commands'

For this example we add description to interface GigabitEthernet0/1.
Commands send as list with delimiter - ','.

commands file:

```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker
AddEntIf0/1Desc;interface GigabitEthernet0/1,description Test,exit;conf_set;1;prompt;;
WriteM;write memory;;1;OK;simple;Ok,Attention!
```

Output:

```
------------------------------------------
| CmdName         | Result                    |
|:----------------|:--------------------------|
| AddEntIf0/1Desc | [search: prompt, count: 1] |
| WriteM          | Ok [ OK]                  |
```

[Use cases]
---

#### 5.2. Configuration device in mode 'command by command'

For this example we add description to interface GigabitEthernet0/1 command by command.

This is may be useful if you want to check for example syntax each command. 

commands file:

```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker
EntConf;conf t;conf_enter;1;prompt;count;
interface_GigabitEthernet0/1; interface GigabitEthernet0/1;conf_cmd;1;prompt;count;
description;  description Test;conf_cmd;1;prompt;count;
exit;exit;conf_cmd;1;prompt;count;
ExitConf;exit;conf_exit;;prompt;count;
WriteMem;write memory;general;5;OK;simple;Ok,Attention!
```

Output:

```
------------------------------------------
| CmdName                      | Result                     |
|:-----------------------------|:---------------------------|
| EntConf                      | [search: prompt, count: 1] |
| interface_GigabitEthernet0/1 | [search: prompt, count: 1] |
| description                  | [search: prompt, count: 1] |
| exit                         | [search: prompt, count: 1] |
| ExitConf                     | [search: prompt, count: 1] |
| WriteMem                     | Ok [ OK]                   |
```

[Use cases]
---

### 5.3. Configuration device in mode 'basic configuration template'

For this example we add description to interface GigabitEthernet0/1 using prepared template that set as argument.
Variables {if} and {descr} in template will be with replaced by values that set in CLI parameter 'conf_template_var'.

CLI:

```
./autodcr.py -nodes_type csv -nodes nodes.csv -commands /examples/commands_conf_template.csv -conf_template /examples/template.tpl -conf_template_var '{"if": "1", "descr": "Test_script"}'
```

commands file:

```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker
Config;;conf_tpl;1;prompt;;
WriteM;write memory;;1;OK;simple;Ok,Attention!
```

template.tpl:

```
interface GigabitEthernet0/{if}
 description Test_script{descr}
exit
```

Output:

```
   Node name: router_1

------------------------------------------
| CmdName      | Result                     |
|:-------------|:---------------------------|
| Config       | [search: prompt, count: 1] |
| WriteM       | Ok [ OK]                   |
```

[Use cases]
---

#### 5.5. Configuration device in mode 'configuration template per command with table of variables'

For this example we add description to interface GigabitEthernet0/1 using prepared template that set in section 'command'.

Variables {if} and {descr} in template will be with replaced by values that regarding to current node.

commands file:

```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker
Config;template.tpl,varlist.csv;conf_tpl;1;prompt;simple;Ok,Error!
WriteM;write memory;;1;OK;simple;Ok,Error!
```

template.tpl:

```
interface GigabitEthernet0/{if}
 description Test_script{descr}
exit
```

varlist.csv:

```
nodename;if;descr
Node_L;1;Left
Node_R;1;Right
```

Output:

```
   Node name: Node_L

------------------------------------------
| CmdName   | Result                     |
|:----------|:---------------------------|
| Config    | [search: prompt, count: 1] |
| WriteM    | Ok [ OK]                   |

==========================================

   Node name: Node_R

------------------------------------------
| CmdName   | Result                     |
|:----------|:---------------------------|
| Config    | [search: prompt, count: 1] |
| WriteM    | Ok [ OK]                   |
```

[Use cases]
---

#### 5.6. Configuration device in mode 'configuration template per command with table of variables  and nodename'

For this example we add description to interface GigabitEthernet0/1 using prepared template that set in section 'command'.

For this example will be replaced variable {if} and {descr} using set of variables for 'Node_L' (connected nodename will not be used)

This is may be useful if you want to configure another node connected through ssh.

commands file:

```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker
Config;template.tpl,varlist.csv,Node_L;conf_tpl;1;prompt;simple;Ok,Error!
WriteM;write memory;;1;OK;simple;Ok,Error!
```

[Use cases]
---

### 6. Request user for search value

#### 6.1. Request user for search value

For this example we ask user for MAC address that he want to search.

commands file:

```
cmd_type;delay_factor;search;search_type;result_marker
Request search value;Enter search value:;usr_req;;;;
Get MAC;show arp;;;\S+\s+(?P<IPaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+\S+\s+(?P<MAC>(?:\S)*{usr_req}(?:\S)*)\s+\S+\s+(?P<Interface>.*);complex;Ok,Err;
```

Output:

```
[router_1] Connection to device 192.168.1.1
[router_1] Try to execute command: Enter search value: on device: 192.168.1.1:
[router_1] Enter search value:5897.1e9a.afd8
[router_1] Check command Enter search value: for error
[router_1] Command: Enter search value: on device: 192.168.1.1 executed successfully
[router_1] Try to execute command: show arp on device: 192.168.1.1:
[router_1] Check command show arp for error
[router_1] Command: show arp on device: 192.168.1.1 executed successfully
Start report:
Generation full report.....
Full report generated
Start preparing summary report.....
Summary report prepared
Summary report:

==========================================

   Node name: router_1



------------------------------------------
| CmdName              | Result|
|:---------------------|:--------------------------------------------------|
| Request search value | [ 5897.1e9a.afd8]|
| Get MAC              | Ok [result:
                         command:show arp
                         +-----------------+----------------+---------------------+
                        | IPaddress        | MAC            | Interface           |
                        +==================+================+=====================+
                        | 192.168.1.100    | 5897.1e9a.afd8 | GigabitEthernet0/23 |
                        +------------------+----------------+---------------------+] 

==========================================

```

[Use cases]
---

#### 6.2. Request user for set of variables

For this example we search l2vpn state 'DOWN' than ask user for what is set of variable send for use in next command from result of execution command.
 
commands file:

```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker
l2vpn status;Sho l2vpn atom vc;;1;(?P<If>\S+)\s+(?P<PeerID>\S+)\s+(?P<vcid>\d+)\s+\S+\s+(?P<Name>\S+)\s+DOWN;complex; Err !,Ok
Choose search value;Choose search value:;choose_req;;;;
l2vpn status detail;Sho l2vpn atom vc vcid {vcid} detail;;1;(?P<Line>.*)(?P<Status>DOWN);complex; Err !,Ok
```

Output:

```
[router_1] Connection to device 192.168.1.2
[router_1] Try to execute command: Sho l2vpn atom vc on device: 192.168.1.2:
[router_1] Check command Sho l2vpn atom vc for error
[router_1] Command: Sho l2vpn atom vc on device: 192.168.1.2 executed successfully
[router_1] Try to execute command: Choose search value: on device: 192.168.1.2:
[router_1] Choose search value:
|   N | If       | PeerID         |   vcid | Name                  |
|----:|:---------|:---------------|-------:|:----------------------|
|   0 | pw100541 | 192.168.1.199  |   3070 | l3vpn_TestCase4_3070  |
|   1 | pw100663 | 192.168.1.199  |   3221 | l3vpn_TestCase3_3221S |
[router_1] Enter number of line:0
[router_1] Check command Choose search value: for error
[router_1] Command: Choose search value: on device: 192.168.1.2 executed successfully
[router_1] Try to execute command: Sho l2vpn atom vc vcid 3070 detail on device: 192.168.1.2:
[router_1] Check command Sho l2vpn atom vc vcid 3070 detail for error
[router_1] Command: Sho l2vpn atom vc vcid 3070 detail on device: 192.168.1.2 executed successfully
Start report:
Generation full report.....
Full report generated
Start preparing summary report.....
Summary report prepared
Summary report:

==========================================

   Node name: router_1

------------------------------------------
| CmdName              | Result|
|:---------------------|:--------------------------------------------------|
| l2vpn status         | Err ! [result:
                         command:Sho l2vpn atom vc
                         +----------+---------------+--------+-----------------------+
                        | If       | PeerID         |   vcid | Name                  |
                        +==========+================+========+=======================+
                        | pw100541 | 192.168.1.199  |   3070 | l3vpn_TestCase4_3070  |
                        +----------+----------------+--------+-----------------------+
                        | pw100663 | 192.168.1.199  |   3221 | l3vpn_TestCase3_3221S |
                        +----------+----------------+--------+-----------------------+] |
| Choose search value  | No search values|
| l2vpn status detail  | Err ! [result:
                         command:Sho l2vpn atom vc vcid 3070 detail
                         +---------------------------------------------------------+----------+
                        | Line| Status   |
                        +=========================================================+==========+
                        | Targeted Hello: 192.168.1.99(LDP Id) -> 192.168.1.199, LDP is | DOWN     |
                        +---------------------------------------------------------+----------+]|

==========================================
```

[Use cases]
---

### 7. RestAPI

#### 7.1. Get nodes

This GET method return all nodes from group cisco_ios. 

Using for checking correct node configurations.

Example:

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

[Use cases]
---

#### 7.2. Get cmd

This GET method executing commands for nodes and returns report.

For this example we will do:
- connect to the node1;
- use parameter 'conf_template' as source of configuration template;
- use parameter 'conf_template_var' as source of variables value for replacing in tempate;
- congigure description to interface GigabitEthernet0/1
						
Example:

```
http://192.168.1.7:9090/cmd?group=cisco_ios&name=node1&par=cisco_ios_par&commands=commands_conf_template.csv&conf_template=interface GigabitEthernet{if}\n description {descr}\nexit&conf_template_var={"if": "0/1", "descr": "Test_script"}


Summary report:

==========================================

   Node name: node1

------------------------------------------
| CmdName      | Result                    |
|:-------------|:--------------------------|
| Config       | [search: prompt, count: 1] |
| WriteM       | Ok [ OK]                  |

==========================================
```

[Use cases]
---

### 8. Export result

#### 8.1. Export result of command execution to excel

For this example we search cdp neighbors and interface status 'disabled|connected|notconnect' and than export result tables to the exel.

Can be exported any result that be in table format.

This is may be useful if you want to do some in inventory.

CLI:

```
/autodcr.py -nodes nodes.csv -commands migr/inventory/commands_inventory.csv -export excel
```

commands file:

```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker
Neighbors;show cdp neighbors detail;;1;Device ID: (?P<DeviceID>.*)\n.*\n  IP address: (?P<IPaddress>.*)\nPlatform: (?P<Platform>.*),.*\nInterface: (?P<Local>.*),.*\(outgoing port\): (?P<Outgoing>.*);complex;
Interfaces;show interface status;;1;(?P<Port>\w{2}\d\S+)(?P<Name>.*)(?P<Status>disabled|connected|notconnect)\s+(?P<Vlan>\S+).*\n;complex;
```

Output:

```
------------------------------------------
| CmdName    | Result|
|:-----------|:--------------------------------------------------|
| Neighbors  | [result:
                         command:show cdp neighbors detail
                         +---------------------------+-------------+-----------------------+---------------------+------------------------+
                        | DeviceID  | IPaddress      | Platform              | Local               | Outgoing               |
                        +============================+=============+=======================+=====================+========================+
                        | router_R  | 192.168.1.101  | cisco ASR9K Series    | GigabitEthernet0/10 | GigabitEthernet0/0/0/0 |
                        +----------------------------+-------------+-----------------------+---------------------+------------------------+
                        | router_L  | 192.168.1.102  | cisco ME-3800X-24FS-M | GigabitEthernet0/23 | GigabitEthernet0/23    |
                        +----------------------------+-------------+-----------------------+---------------------+------------------------+]|
| Interfaces | [result:
                         command:show interface status
                         +--------+--------------------+------------+--------+
                        | Port   | Name               | Status     | Vlan   |
                        +========+====================+============+========+
                        | Gi0/1  | Test_scriptRight   | notconnect | 1      |
                        +--------+--------------------+------------+--------+
                        | Gi0/2  |                    | notconnect | 1      |
                        +--------+--------------------+------------+--------+
                        | Gi0/3  | temp_mgt           | disabled   | 1      |
                        +--------+--------------------+------------+--------+
] |

==========================================
```

[Use cases]
---

#### 8.2. Export result of command execution to word

For this example we send commands to the node and then export outputs to prepared word template.

This is may be useful if you want to do some in report.

CLI:

```
/autodcr.py -nodes nodes.csv -commands migr/inventory/commands_report.csv -export word
```

commands file:

```
cmdname;command;cmd_type;delay_factor;search;search_type;result_marker
show_version;show version;;1;prompt;count;
show_clock;show clock;;1;prompt;count;
show_users;show users;;1;prompt;count;
show_license_feature;show license feature;;1;prompt;count;
show_license_status;show license status;;1;prompt;count;
show_license_statistics;show license statistics;;1;prompt;count;
```

[Use cases]

===

[Home](../README.md)

[1]: usecases.md#1-search
[11]: usecases.md#11-search-mac-address
[12]: usecases.md#12-cdp-neighbors-discovery
[13]: usecases.md#13-version-and-serial-number-discovery
[14]: usecases.md#14-ping-with-sort-mode-command
[15]: usecases.md#15-check-port-status
[16]: usecases.md#16-check-predefined-status
[17]: usecases.md#17-check-protocol-and-use-result-marker
[2]: usecases.md#2-log-parsing
[21]: usecases.md#21-log-parsing-flapping
[22]: usecases.md#22-log-parsing-select-last-message
[3]: usecases.md#3-use-search-as-value
[31]: usecases.md#31-command-chain-imple
[32]: usecases.md#32-command-chain-complex
[33]: usecases.md#33-send-result-of-execution-previous-command-to-shell-OS-command
[4]: usecases.md#4-build-in-command-and-variables
[41]: usecases.md#41-use-timeout-for-execution-commands
[42]: usecases.md#42-use-build-in-variables-backup
[43]: usecases.md#43-ssh-connections-through-device-to-another-device
[5]: usecases.md#5-configuration-device
[51]: usecases.md#51-configuration-device-in-mode-list-of-commands
[52]: usecases.md#52-configuration-device-in-mode-command-by-command
[53]: usecases.md#53-configuration-device-in-mode-basic-configuration-template
[54]: usecases.md#54-configuration-device-in-mode-configuration-template-per-command
[55]: usecases.md#55-configuration-device-in-mode-configuration-template-per-command-with-table-of-variables
[56]: usecases.md#56-configuration-device-in-mode-configuration-template-per-command-with-table-of-variables--and-nodename
[6]: usecases.md#6-request-user-for-search-value
[51]: usecases.md#61-request-user-for-search-value
[52]: usecases.md#62-request-user-for-set-of-variables
[7]: usecases.md#7-restapi
[71]: usecases.md#71-get-nodes
[72]: usecases.md#72-get-cmd
[8]: usecases.md#8-export-result
[81]: usecases.md#81-export-result-of-command-execution-to-excel
[82]: usecases.md#82-export-result-of-command-execution-to-word

[Use cases]: usecases.md#use-cases