# -*- coding: utf-8 -*-

# with open("t1.txt", "r") as code:
#     # r =  code.read()
#     print code
#     i = code.read()
#     print dict(i)
# print r
import glob
import random
# print glob.glob(r"E:\CarcerWorld\code\Python\git\image_str\image_server\wx_app\lib\robote/*.gif")
# all =  glob.glob(r"E:\CarcerWorld\code\Python\git\image_str\image_server\wx_app\lib\robote/*.gif")
# for filename in :
#     print filename

# print int(random.random()*(len(all)-1))

import subprocess
_cmd = u'python H:\Code\Python\Git\image_str\image_server\wx_app\lib/robote/test1.py  '

subproc = subprocess.Popen(_cmd,  stdin=subprocess.PIPE,shell=True)
print('start')
subproc.stdin.write('data\n')
subproc.communicate('data\n')
print('end')