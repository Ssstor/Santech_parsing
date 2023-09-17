import subprocess

command = 'docker run -t docker_parser'

try:
    result = subprocess.check_output(command, shell=True).decode('utf-8')
    print(result)
except:
    command = 'docker build -t docker_parser docker_parser'
    result = subprocess.check_output(command, shell=True).decode('utf-8')
    subprocess.check_output('docker run -t docker_parser', shell=True).decode('utf-8')
    print(result)
 
