#!/usr/bin/python

import os
import re

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

class FmtInfo(object):
    '''Encapsulates formatting information, such as
    column widths and table headers
    '''
    # table headings...
    PID_HEADING     = 'PID'
    PPID_HEADING    = 'PPID'
    CMD_HEADING     = 'COMM'
    UTIME_HEADING   = 'UTIME'
    THREADS_HEADING = 'NUM_THREADS'
    CPU_HEADING     = 'CPU'
    VSIZE_HEADING   = 'VSIZE'

    # maximum width for the `comm` column
    MAX_CMD_WIDTH = 15;

    def __init__(self):
        '''Initializes column widths'''
        self.pid_width     = len(FmtInfo.PID_HEADING)
        self.ppid_width    = len(FmtInfo.PPID_HEADING)
        self.cmd_width     = len(FmtInfo.CMD_HEADING)
        self.utime_width   = len(FmtInfo.UTIME_HEADING)
        self.threads_width = len(FmtInfo.THREADS_HEADING)
        self.cpu_width     = len(FmtInfo.CPU_HEADING)
        self.vsize_width   = len(FmtInfo.VSIZE_HEADING)

    def relayout(self, info):
        '''Recalculates the layout based on `info`.
        This essentially just expands columns as necessary
        '''
        self.pid_width     = max(self.pid_width, len(info.pid))
        self.ppid_width    = max(self.ppid_width, len(info.ppid))

        # always truncate to MAX_CMD_WIDTH
        self.cmd_width     = min(max(self.cmd_width, len(info.cmd)), FmtInfo.MAX_CMD_WIDTH)
        self.utime_width   = max(self.utime_width, len(info.utime))
        self.threads_width = max(self.threads_width, len(info.num_threads))
        self.cpu_width     = max(self.cpu_width, len(info.cpu))
        self.vsize_width   = max(self.vsize_width, len(info.vsize))

    def fmt_width(self, string, width):
        '''Formats `string` to have width `width`, padding/truncating as necessary'''
        str_width = len(string)
        if str_width > width:
            # truncate and add elipsis
            return string[:width-3] + '...'
        else:
            # pad with spaces
            return string + ' ' * (width-str_width)

    def print_headings(self):
        '''Prints headings for the table'''
        print (self.fmt_width(FmtInfo.PID_HEADING, self.pid_width) + '   '
               + self.fmt_width(FmtInfo.PPID_HEADING, self.ppid_width) + '   '
               + self.fmt_width(FmtInfo.CMD_HEADING, self.cmd_width) + '   '
               + self.fmt_width(FmtInfo.UTIME_HEADING, self.utime_width) + '   '
               + self.fmt_width(FmtInfo.THREADS_HEADING, self.threads_width) + '   '
               + self.fmt_width(FmtInfo.CPU_HEADING, self.cpu_width) + '   '
               + self.fmt_width(FmtInfo.VSIZE_HEADING, self.vsize_width))

    def print_row(self, info):
        '''Prints a row in the table'''
        print (self.fmt_width(info.pid, self.pid_width) + '   '
               + self.fmt_width(info.ppid, self.ppid_width) + '   '
               + self.fmt_width(info.cmd, self.cmd_width) + '   '
               + self.fmt_width(info.utime, self.utime_width) + '   '
               + self.fmt_width(info.num_threads, self.threads_width) + '   '
               + self.fmt_width(info.cpu, self.cpu_width) + '   '
               + self.fmt_width(info.vsize, self.vsize_width))

def is_pid(name):
    '''Returns whether name is a valid pid'''
    return re.compile('^[0-9]+$').search(name)

def ps():
    '''Main function: gathers information about all running
    processes and prints it in a table
    '''
    fmt = FmtInfo()
    proc_info = []

    # pass 1: gather info & formatting
    for pid in filter(is_pid, os.listdir('/proc')):
        info = ProcInfo(pid)
        fmt.relayout(info)
        proc_info.append(info)

    # pass 2: print table
    fmt.print_headings()
    for info in proc_info:
        fmt.print_row(info)

if __name__ == '__main__':
    ps()
