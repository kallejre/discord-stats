import os, sys, subprocess
#os.system('python3 ./bot4.6')

os.chdir(os.path.abspath("."))
print(os.system("echo %CD%"))

os.system('python bot4.7.py')
subprocess.call(sys.executable + ' "' + os.path.realpath(__file__) + '"')
