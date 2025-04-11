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
    "Set up argparse here. Call this function inside main."
    parser = argparse.ArgumentParser(description="DU Improved -- See Disk Usage Report with bar charts",epilog="Copyright 2022")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    # add argument for "human-readable". USE -H, don't use -h! -h is reserved for --help which is created automatically.
    # check the docs for an argparse option to store this as a boolean.
    # add argument for "target". set number of args to 1.
    parser.add_argument("target", nargs="?", default=".", help="The target directory")
    return parser.parse_args()


def percent_to_graph(percent, total_chars):
    "returns a string: eg. '##  ' for 50 if total_chars == 4"
    "THis function checks if percent is between 0 and 100"
    "And converts the percent to graph using the = character and empty spcae."

    if not (0 <= percent <= 100):
        raise ValueError("Percent must be between 0 and 100.")
    filled = round((percent / 100) * total_chars)
    empty = total_chars - filled
    return "=" * filled + " " * empty

def call_du_sub(location):
    "takes the target directory as an argument and returns a list of strings"
    "returned by the command `du -d 1 location`"
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
    "gets a list from call_du_sub, returns a dictionary which should have full"
    "directory name as key, and the number of bytes in the directory as the value."
    pass


if __name__ == "__main__":
    args = parse_command_args()
    dir_list = call_du_sub(args.target)
    print(dir_list)

