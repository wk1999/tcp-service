#!/usr/bin/env python
import os, sys, getopt
import json


def usage():
    print '''
Usage:
    -h
    -l
    -e
    '''

def debug_args(args, desc = 'args'):
    print '\n***' + desc + '***'
    i = 0
    for arg in args:
        print 'arg' + str(i) + ': ' + arg
        i += 1
    print '******\n'


def load_map(file_path):
    mp = {}
    if not os.path.exists(file_path):
        return mp

    with open(file_path, "r") as f:
        json_str = f.read()
        mp = json.loads(json_str)
    return mp

def write_map(mp, file_path):
    with open(file_path, 'w+') as f:
        json_str = json.dumps(mp)
        f.write(json_str)

###########################

services_file = '/tmp/running_services'
start_app = "tcp_main.py"

def list_running_services():
    services_map = load_map(services_file)
    print services_map

def start_service(service_dir):
    services_map = load_map(services_file)
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
        write_map(services_map, services_file)

def stop_service(service_dir):
    services_map = load_map(services_file)
    if service_dir in services_map:
        cmd = "kill -9 " + str(services_map[service_dir])
        print(cmd)
        os.system(cmd)
        del services_map[service_dir]
        write_map(services_map, services_file)

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
