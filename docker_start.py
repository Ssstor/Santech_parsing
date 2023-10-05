<<<<<<< HEAD
import os 
import argparse


=======
import subprocess
>>>>>>> 1d11231b9ccd71974fdcbf58344c1a10f3e518e1

command = 'docker run -t docker_parser'

try:
    result = subprocess.check_output(command, shell=True).decode('utf-8')
    print(result)
except:
    command = 'docker build -t docker_parser docker_parser'
    result = subprocess.check_output(command, shell=True).decode('utf-8')
    subprocess.check_output('docker run -t docker_parser', shell=True).decode('utf-8')
    print(result)
 
