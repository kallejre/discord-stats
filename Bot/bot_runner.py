import os
import sys
import subprocess

# os.system('python3 ./bot4.6')
os.chdir(os.path.abspath('.'))
try:
    os.system('python3 bot4.7.py')
except SystemExit:
    pass
os.system('python3 bot_runner.py')