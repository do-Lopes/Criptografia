import subprocess
import time

subprocess.Popen('start cmd /k python Server.py', shell=True)
time.sleep(1)
subprocess.Popen('start cmd /k python Client.py', shell=True)
time.sleep(2)
subprocess.Popen('start cmd /k python Client.py', shell=True)