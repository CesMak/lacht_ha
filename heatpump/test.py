#from pymodbus.client.sync_diag import ModbusTcpDiagClient as ModbusClient 
# Port 502 freigegeben in fritzbox und man sieht auch die WWP Anlage dort!
# from pymodbus.client import ModbusTcpClient
# import logging 

# logging.basicConfig() 
# log = logging.getLogger() 
# log.setLevel(logging.DEBUG)

# WWP = ModbusTcpClient(host='192.168.178.051', port=502) #84.177.30.219
# WWP.read_input_registers(42103, unit=1)

from pymodbus.client import ModbusTcpClient
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

WWP = ModbusTcpClient(host='192.168.178.51', port=502) # works with .51 do not use 051
testconnect = WWP.connect()
print(testconnect)
rr = WWP.read_input_registers(42103, 1)