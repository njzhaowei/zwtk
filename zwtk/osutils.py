import os
import re
import subprocess
import platform
from pathlib import Path
from .fileutils import writefile

def ismac():
    return (platform.system() == 'Darwin')

def iswin():
    return (platform.system() == 'Windows')

def islinux():
    return (platform.system() == 'Linux')

def write_pidfile(dir='.'):
    pid = os.getpid()
    pth = Path(dir) / ('%s.pid'%pid)
    Path(pth).parent.mkdir(parents=True, exist_ok=True)
    writefile(pth, pid)
    return pth

def run_shell(cmd, *args):
    cmds = [cmd]
    cmds.extend(list(args))
    r = subprocess.run(cmds, stdout=subprocess.PIPE).stdout.decode('utf-8')
    return r