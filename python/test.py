#!/usr/bin/env python
import sys
from trakr import trakr

args = sys.argv
if len(args) == 1:
    raise Exception('Please enter at least one argument create | test to run the script')

if args[1] == 'create':
    tester = trakr()
    tester.createProject()
else:
    tester = trakr()
    tester.runTest()
