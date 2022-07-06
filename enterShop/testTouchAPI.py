import os
import sys
sys.path.append(os.pardir)

import srvclt
import touchAPI
import comutil

touchAPI.setup()
print('Welcome!!!')
clt = srvclt.Client("192.168.0.7")
clt.prepareSocket()
clt.run()
while True:
    count=touchAPI.count()
    if count==0:
        break
    unit = comutil.ComUnit(9 ,"192.168.0.5", None, count)
    clt.send(unit)
touchAPI.end()
clt.disconnect()