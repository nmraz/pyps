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
    '''Enumerates all running processes and calls cb with the pid of each one'''
    for name in filter(is_pid, os.listdir('/proc')):
        cb(name)


class ProcInfo(object):
    '''Holds information about a process, including:
        * pid - self.pid
        * ppid - self.ppid
        * command line - self.cmd
        * thread count - self.num_threads
        * virtual memory size - self.vsize
        * cpu - self.cpu
        * utime - self.utime
    '''
    def __init__(self, pid):
        '''Extracts information about a process based on its pid'''
        self.pid = pid
        with open('/proc/' + pid + '/stat') as stat:
            data = stat.read().split()
        self.ppid        = data[3]
        self.cmd         = data[1][1:-1]  # remove parentheses from name
        self.utime       = data[13]
        self.num_threads = data[19]
        self.cpu         = data[38]
        self.vsize       = data[22]





