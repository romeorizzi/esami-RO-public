import sys

#Blocca python versioni di python inferiori a 2
if sys.version_info[0] <= 2:
    print("Questo script richiede python 3 installato in un Conda Environment")
    exit()

import os
import subprocess
import webbrowser
import signal
import socket
import importlib
if sys.version_info[1] > 4:
    from importlib import util
 
conda_environment = sys.argv[1] if len(sys.argv) == 2 else "ROexam"
webserverPort = 8080
webserverIp = "127.0.0.1"
start_port = 8888
pythonPath = sys.executable

print(
    "=================================\n" +
    "Python versione " + str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "\n" + 
    "Sistema Operativo: " + str(sys.platform) + "\n" + 
    "Percorso: " + str(sys.exec_prefix) + "\n" + 
    "=================================\n"
)

# Check conda environment
if conda_environment not in sys.exec_prefix:
    print("ATTENZIONE:\nEsegui questo script dal giusto conda environment: " + conda_environment)
    exit()
    

def module_exists(name):
    if sys.version_info[0] == 3:
        if sys.version_info[1] <= 4:
            return importlib.find_loader(name) is not None
        else:
            return importlib.util.find_spec(name) is not None
    return False

# Check di avvio
if not module_exists("notebook"):
    print("ATTENZIONE:\nIl modulo notebook non esiste, accertarsi di eseguire questo script dal corretto conda environment")
    exit()

# Cerca una porta libera su cui eseguire jupyter
def tryPort(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ret = False
    try:
        sock.bind(("127.0.0.1", port))
        ret = True
    except:
        print("Porta "+str(port)+" in uso, ")
        ret = False
    sock.close()
    return ret

target_port = start_port
while not tryPort(target_port):
    target_port += 1

jupyterPort = str(target_port)
print("La porta che verra' utilizzata per Jupyter e': " + jupyterPort + "\n")


conda_env_path = sys.exec_prefix

# start jupyter notebook
proc_jupyter = subprocess.Popen(["python", '-m', 'notebook', "--NotebookApp.token=''", "--no-browser", "--port", jupyterPort])

target_port = webserverPort
while not tryPort(target_port):
    target_port += 1

webserverPort = str(target_port)
print("La porta che verra' utilizzata per il Server e': " + webserverPort + "\n")

# start local http server
# command = sys.executable + " map/server.py " + str(webserverPort) + " --bind " + webserverIp 
# print("> " + command)
# proc_server = subprocess.Popen(command, shell=True)

proc_server = subprocess.Popen(["python", "map/server.py", webserverPort, "--bind", webserverIp])
webbrowser.open("http://" + webserverIp + ":" + webserverPort + "/map/index.html?port="+jupyterPort)

try:
    proc_jupyter.communicate()
    proc_server.communicate()
    print("COMMUNICATED")
except KeyboardInterrupt:
    proc_jupyter.terminate()
    proc_server.terminate()
    print("\n----Closing program---\n")
    proc_close_jupyter = subprocess.Popen(["python", "-m", "notebook", "stop", jupyterPort])
