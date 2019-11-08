#!/usr/bin/env python

import sys, os, time
import json_map

if __name__ == '__main__':
    service_file = sys.argv[1]
    service_map = json_map.load(service_file)
    while len(service_map) > 0:
        items = service_map.items()
        for service_name, service_pid in items:
            cmd = "kill -0 " + str(service_pid)
            res = os.system(cmd)
            if res != 0:
                print(service_name, "DEAD")
                del service_map[service_name]
                json_map.write(service_map, service_file)
        time.sleep(1)
        service_map = json_map.load(service_file)
