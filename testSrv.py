import srvclt

srv = srvclt.Server()
srv.prepareSocket()
print('Server is running...')
srv.run()