import os
import codecs
import shutil

def rmfile(pth):
    if os.path.isfile(str(pth)):
        os.remove(str(pth))

def rmdir(pth):
    shutil.rmtree(str(pth), ignore_errors=True)

def writefile(pth, txt, enc='utf-8'):
    with codecs.open(pth, 'w', enc) as fp:
        fp.write(txt)
        fp.flush()

def readfile(pth, enc='utf-8', default=None):
    rtn = None
    with codecs.open(pth, 'r', enc) as fp:
        rtn = fp.read()
    if rtn.startswith('\ufeff'):# BOM
        rtn = rtn[1:]
    return rtn
