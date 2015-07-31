import sys
import fcntl
import os
import re
import logging
import time

from datetime import datetime

import requests

logging.basicConfig(filename='debug.log',level=logging.DEBUG,
    format='%(asctime)s.%(msecs)d %(levelname)s %(module)s - %(funcName)s: %(message)s', 
    datefmt="%Y%m%d %H:%M:%S")
logging.info('Start logging')

urlroot='http://api.thethings.io/v2/things/'
token='efO4K0dp-A84_gNhmkd_ohKIBu3wCD2AseIWsHn51GA'
header={'Accept': 'application/json', 'Content-Type': 'application/json'}
url=urlroot+token

def ttwrite(var, value):
    if int(value) > 4400:
        logging.warning('!!!Too big value: ' + value)
        return
    data='{"values":[{"key": "' + var + '","value": "' + value + '"}]}'
    #r = requests.post(url, headers=header, data=data)
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    odate = datetime.now().strftime("%Y%m%d")
    print var, value, date
    text_file = open("data-"+odate+".log", "a")
    text_file.write("%s %s %s\n" % (var,value, date)) 
    text_file.close()


last=0
# make stdin a non-blocking file
fd = sys.stdin.fileno()
fl = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

# user input handling thread
while True:
    try: input = sys.stdin.readline()
    except: continue
    time.sleep(0.1)
    #var = input[25:-1]

    if (len(input)>0):
        logging.debug('Input-> ' + input[:-1])    
        m = re.match("current watts \(230v\)   = (?P<wa>\d+)", input)
        if m:
            var = m.group("wa")
            if (var!=last):
                ttwrite('Watts', var)
                last = var

