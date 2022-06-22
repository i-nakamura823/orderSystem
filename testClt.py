import srvclt

clt = srvclt.Client(input())
clt.prepareSocket()
clt.run()