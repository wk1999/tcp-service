#!/usr/bin/env python
import tcp_server
import service
import sys, getopt

default_module = 'my_service'
default_class  = 'service'

def usage():
    print '''
Usage:
    -d     service directory          (mandatory)
    -m     service module name        [default = %s]
    -c     service class  name        [default = %s]
    -h     show this help
    ''' % (default_module, default_class)

if __name__ == '__main__':
    service_directory = None
    service_module = default_module
    service_class = default_class

    opts, _ = getopt.getopt(sys.argv[1:], "hd:m:c:")
    for op, value in opts:
        print(op, value)
        if op == '-m':
            service_module = value
        elif op == '-c':
            service_class = value
        elif op == '-d':
            service_directory = value
        elif op == '-h':
            usage()
        else:
            print("Oh I cannot see it")

    if not service_directory:
        usage()
        exit(-1)

    print("service:[%s.%s.%s]" %(service_directory, service_module, service_class))
    service_instance = service.service(service_module, service_class)
    if service_instance.load(service_directory):
        print("server running with service:", service_instance.name())
        server = tcp_server.tcp_server(service_instance)
        server.run()
    else:
        print("service load failed")
        exit(-1)
