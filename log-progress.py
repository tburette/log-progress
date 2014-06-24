#! /usr/bin/env python
import argparse
import datetime
import time
import re
import sys

def output_app_message(file, delta, message, time):
    print >>file, "{0}>>{1} @ {2}".format(
        delta, 
        message,
        time)

def delta_since(start_date):        
    delta =  datetime.datetime.now() - start_date
    #second level precision
    delta = delta - datetime.timedelta(microseconds=delta.microseconds)
    return delta

def run(start_date, file):
    while True:
        #delta_since must be after raw_input 
        #to compute date at which text was input
        input = raw_input(">")
        output = "{1}> {0}".format(
            input,
            delta_since(start_date))
        print output
        if input.strip().lower() != "time":
            print >>file, output
        file.flush()

def parse_args():
    parser = argparse.ArgumentParser(
        description="Gauge your productivity by writing down when you " + 
        "accomplished a new task. Review progress later.")
    parser.add_argument(
        'file',
        type=argparse.FileType('a+'),
        nargs='?',
        default='out.log',
        help="File to write to")
    return parser.parse_args()

def read_last_delta(file_name):
    #quick and dirty
    lines = open(file_name, 'r').readlines()
    lines.reverse()
    for line in lines:
        #should use strptime
        match = re.match(r'^(\d*):(\d{1,2}):(\d{1,2})>', line)
        if(match):
            ints = [int(x) for x in match.groups()]
            seconds = ints[0]*60*60 + ints[1]*60 + ints[2]
            return datetime.timedelta(seconds=seconds)
    return None

def compute_start_date(file_name):
    last_delta = read_last_delta(file_name)
    if last_delta:
        return datetime.datetime.now() - last_delta
    else:
        return datetime.datetime.now()

if __name__ == '__main__':
    global args
    args =  parse_args()
    start_date = compute_start_date(args.file.name)
    try:
        output_app_message(
            args.file, 
            delta_since(start_date),
            "Start", 
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        run(start_date, args.file)
    finally:
        #BUG: try to write even if problem with the output file, 
        #parsing or a fatal error
        output_app_message(
            args.file, 
            delta_since(start_date),
            "Stop", 
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
