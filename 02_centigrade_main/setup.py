# run this script once to install all dependencies
import os
import platform

platform_name = platform.system()

def install_requirements():
    if platform_name == 'Linux':     
        os.system('apt install python3-pip')
        os.system('pip3 install -r requirements.txt')
    if platform_name == 'Darwin':
        os.system('pip3 install -r requirements.txt')
    if platform_name == 'Windows':
        os.system('pip install -r requirements.txt')

