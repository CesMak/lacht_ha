# Heatpump
   * [Setup Weißhaupt indor unit](#setup-weißhaupt-indor-unit)
   * [Setup Home assistant](#setup-home-assistant)
   * [Modbus configuration](#modbus-configuration)

![alt text](doc/overview.png)

Here I share how to integrate a **Weißhaupt Split-HeatPump** (Weißhaupt Split-Wärmepumpe) into the Home Assistnat. My *.yaml files work perfectly for the **WWP-LS-10-BR** however also for the Biblock etc. you can try my work (it might be however that you do have some other parameters availalbe this also depends on your WWP-CPU Version). My work is inspired by [this forum](https://community.home-assistant.io/t/weishaupt-heatpump-integration-via-modbus/436823/144)

## Setup Weißhaupt indor unit
* Weißhaupt WWP LS 10 BR
* Version WWP-SG V3.0 (see under: )
* Version WWP-CPU V5.2 (see under: )
* in order to use Modbus TCP you need version >=4
* in other versions you do not have the Modubs TCP tile:
![alt text](doc/setup.png)
* connect the LAN / Modbus connection to your indoor unit
* setup TCP connection as above (you can choose another ip as well but make sure to be consistent)
* on your router (fritz box) activate port 502 (Portfreigabe) for your Weißhaupt heatpump it should be named *WWP-CPU-....*.
* For a basic connection test try to ping to your ip:
```bash
ping 192.168.178.051
```
* Additionally you can also try this python code:
```python
from pymodbus.client import ModbusTcpClient
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

WWP = ModbusTcpClient(host='192.168.178.51', port=502) # works with .51 do not use 051
testconnect = WWP.connect()
print(testconnect)
rr = WWP.read_input_registers(42103, 1)
```

## Setup Home assistant
With [Home Assistant](https://www.home-assistant.io/)(HA) you can display your heatpump data in a nice way. Besides that you can of course also use ioBroker, python scripts (see above), or other smart home software.
Here I explain only how to do it using HA.
* Download and install HA as docker or as full OS on a home server pc (that has to run full time!)
* in HA: Settings Apps -> install *Studio Code Server* or *File editor*
* open Studio Code Server and make sure your files look like mine:
    + *[configuration.yaml](code/configuration.yaml)*
    + *[secrets.yaml](code/secrets.yaml)* create this file if it does not exist.
    + *[integrations/modbus_heatpump.yaml](code/modbus_heatpump.yaml)*
    + *[integrations/templates_heatpump.yaml](code/templates_heatpump.yaml)*
* in HA -> overview -> edit dashboard -> Raw configuration editor:
    + *[heatpump_dashboard.yaml](code/heatpump_dashboard.yaml)*
* HA -> Settings -> (dots upper right) -> Restart (do a full restart!)
* HA -> Overview now you should see your dashboard displaying the values of your weißhaupt heatpump (see impressions)

## Modbus configuration
for the modbus addresse's see the **[weißhaupt WWP modbus list](modbus_wwp.xlsx)** you can open this file also with libre office.

## Impressions
heatpump_dashboard.yaml:
![alt text](doc/heatpump_dashboard.png)

you can increase other views
![alt text](doc/tmp.png)


<!-- 
## TODO
* TODO teste aus werte zu veraendern!
* modbus parameter in execl kommentieren und nachschlagen was diese bedeuten
* take a look at errocodes.yaml
* save data to a db? how long is the data stored in HA? 
-->