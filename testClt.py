import srvclt
import re
from comutil import ComUnit

print('please input the client IP Address')
clt = srvclt.Client(input('> '))
clt.prepareSocket()
clt.run()
while True:
    print('input order: menuId, num, reciever IP Address')
    data = input("> ")
    if data == "exit":
        break
    else:
        menuId, num, reciever = re.split('[,\s]+',data)
        unit = ComUnit(reciever = reciever, menuId = menuId, num = num)
    clt.send(unit)
clt.disconnect()

clt.prepareSocket()
clt.run()