import srvclt

print('please input the client IP Address')
clt = srvclt.Client(input())
clt.prepareSocket()
clt.run()