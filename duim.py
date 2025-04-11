#!/usr/bin/env python3

import subprocess, sys
import os
import argparse



'''
OPS445 Assignment 2 - Winter 2022
Program: duim.py 
Author: "Ralph Louisse Tolentino"
The python code in this file (duim.py) is original work written by
"Student Name". No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: This script will implement imporvements when calling du. It will return the contents of a specified directory that will input as argument, and it generate a bar graph for each subdirectory, where the bar graph represents the space used  as percent of the total drive space for the specified directory.

Date: April 11, 2025
'''

def parse_command_args():
    "Returns parse_args information to help users how to use the script. "

    parser = argparse.ArgumentParser(description="DU Improved -- See Disk Usage Report with bar charts", epilog="Copyright 2025")
    parser.add_argument("-H", "--human-readable", action="store_true", help="print sizes in human readable format (e.g. 1K 23M 2G)")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    parser.add_argument("target", nargs="?", default=".", help="The directory to scan.")
    return parser.parse_args()

def percent_to_graph(percent, total_chars):
    "THis function checks if percent is between 0 and 100"
    "And converts the percent to graph using the = character and empty spcae."

    if not (0 <= percent <= 100):
        raise ValueError("Percent must be between 0 and 100.")
    filled = round((percent / 100) * total_chars)
    empty = total_chars - filled
    return "=" * filled + " " * empty

def call_du_sub(location):
    "this fumctioncalls the du command and splits the result into a list"

    try:
        proc = subprocess.Popen(
            ["du", "-d", "1", location],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        stdout, stderr = proc.communicate()

        #added to handle permission denied errors
        if stderr:
            print(f"Warning (du):\n{stderr.strip()}", file=sys.stderr)

        # makes a list from the result
        return [line.strip() for line in stdout.strip().split("\n") if line.strip()]
    except Exception as e:
        raise RuntimeError(f"Subprocess error: {e}")


def create_dir_dict(alist):
    "thus function creates a dictionary of the directory list from call_du_sub"
    dir_dict = {}
    for line in alist:
        try:
            size_str, path = line.split("\t")
            dir_dict[path] = int(size_str)
        except ValueError:
            continue
    return dir_dict

def format_size(size):
    "converts bytes into human-readable format"
    for unit in ['B','K','M','G','T']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} P"

def usage():
    "Print a usage message to the user"
    print("Usage: duim.py -H location")

if __name__ == "__main__":

    if len(sys.argv) < 2:
        usage() #show usage message to user if incomplete arguments
        sys.exit(1)

    args = parse_command_args()

    if not os.path.isdir(args.target):
        print("Error: target must be a valid directory.", file=sys.stderr)
        sys.exit(1)

    dir_list = call_du_sub(args.target)
    dir_dict = create_dir_dict(dir_list)

    total_size = dir_dict.get(args.target, sum(dir_dict.values()))

    sorted_items = sorted(dir_dict.items(), key=lambda x: -x[1])

    for path, size in sorted_items:
        if path == args.target:
            continue
        percent = (size / total_size) * 100
        bar = percent_to_graph(percent, args.length)
        size_str = format_size(size) if args.human_readable else f"{size} B"
        print(f"{percent:>3.0f} % [{bar.ljust(20)}] {size_str.rjust(8)}  {path}")


    total_str = format_size(total_size) if args.human_readable else f"{total_size} B"
    print(f"Total: {total_str:>8}   {args.target}")



