#!/usr/bin/env python
import os, sys, getopt
import json_map

def usage():
    print '''
Usage:
    -h      print this help
    -l      list all running services
    -e <s>  end service <s>
    -d <s>  start service <s>
    '''

def debug_args(args, desc = 'args'):
    print '\n***' + desc + '***'
    i = 0
    for arg in args:
        print 'arg' + str(i) + ': ' + arg
        i += 1
    print '******\n'
###########################

services_file = '/tmp/running_services'
start_app = "tcp_main.py"
monitor_app = "service_monitor.py"

def list_running_services():
    services_map = json_map.load(services_file)
    print services_map

def start_service(service_dir):
    services_map = json_map.load(services_file)
    if service_dir in services_map:
        print('this service already running')
        return

    # start
    pid = os.fork()
    if pid < 0:
        print("how come?")
    elif pid == 0:
        cmd = sys.path[0] + "/" + start_app
        print(cmd)
        os.execv(cmd, sys.argv) ## A wrong value of argv[0] is passed to cmd. No matter today.
        print('assert FAILED')
    else:
        services_map[service_dir] = pid
        json_map.write(services_map, services_file)
        # lauch monotor app when there is only 1 service running(0->1)
        if len(services_map) == 1:
            pid = os.fork()
            if pid < 0:
                print("what bugs?")
            elif pid ==0:
                cmd = sys.path[0] + "/" + monitor_app
                os.execl(cmd, monitor_app, services_file)
                print('assert FAILED')
            else:
                pass

def stop_service(service_dir):
    services_map = json_map.load(services_file)
    if service_dir in services_map:
        cmd = "kill -9 " + str(services_map[service_dir])
        print(cmd)
        os.system(cmd)
        del services_map[service_dir]
        json_map.write(services_map, services_file)

if __name__ == '__main__':
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "hle:d:m:c:")
        for op, value in opts:
            if op == '-h':
                usage()
            elif op == '-l':
                list_running_services()
            elif op == '-e':
                stop_service(value.strip('./'))
            elif op == '-d':
                start_service(value.strip('./'))
    except getopt.GetoptError, err:
        print str(err)
        usage()
