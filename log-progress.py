import argparse
import datetime
import time


def delta_since(start_delta):
    delta =  datetime.datetime.now() - start_delta
    #second level precision
    delta = delta - datetime.timedelta(microseconds=delta.microseconds)
    return delta

def run(file):
    start = datetime.datetime.now()
    while True:
        user_string = raw_input()
        delta = delta_since(start)
        output = "{0}> {1}".format(delta, user_string)
        print output
        print >>file, output

def parse_args():
    parser = argparse.ArgumentParser(
        description="Gauge your productivity by writing down when you " + 
        "accomplished a new task. Review progress later.")
    parser.add_argument(
        'file',
        type=argparse.FileType('a+'),
        help="File to write to")
    return parser.parse_args()

if __name__ == '__main__':
    global args
    args =  parse_args()
    try:
        run(args.file)
    except:
