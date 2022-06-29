import srvclt
import touchAPI
from comutil import ComUnit

touchAPI.setup()
print('Welcome!!!')
clt = srvclt.Client("192.168.0.7")
clt.prepareSocket()
clt.run()
while True:
    count=touchAPI.count()
    if count==0:
        break
    unit = ComUnit(9 ,"192.168.0.7", "192.168.0.7", None, count, None)
    clt.send(unit)
touchAPI.end()
clt.disconnect()