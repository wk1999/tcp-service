#!/usr/bin/env python
import os, json

def load(file_path):
    mp = {}
    if not os.path.exists(file_path):
        return mp

    with open(file_path, "r") as f:
        json_str = f.read()
        mp = json.loads(json_str)
    return mp

def write(mp, file_path):
    with open(file_path, 'w+') as f:
        json_str = json.dumps(mp)
        f.write(json_str)
