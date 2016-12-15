#!/usr/bin/python

import os

def is_pid(name):
    '''Returns whether name is a valid pid'''
    try:
        int(name)  # pids are just integers
        return True
    except ValueError:
        return False

def enum_procs(cb):
    '''enumerates all running processes and calls cb with the pid of each one'''
    for name in filter(is_pid, os.listdir('/proc')):
        cb(name)


# quick test:
def print_pid(pid):
    print pid
enum_procs(print_pid)
