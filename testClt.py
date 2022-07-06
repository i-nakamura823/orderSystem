import srvclt
import re
from comutil import ComUnit

print('please input the client IP Address')
clt = srvclt.Client(input('> '))
clt.prepareSocket()
clt.run()
while True:
    print('input order: mode, menuId, num, reciever IP Address')
    data = input("> ")
    if data == "exit":
        break
    else:
        mode, menuId, num, reciever = re.split('[,\s]+',data)
        unit = ComUnit(int(mode), reciever, int(menuId), int(num))
    clt.send(unit)
clt.disconnect()

clt.prepareSocket()
clt.run()