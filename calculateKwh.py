#!/usr/bin/python
###
# Read instananeous W day file to estimate Kwh
# file format
# UNIT KW DATE(YMDHMS)
# Watts 200 20150719203000
# DATE must be sorted
#
import sys, getopt
import re
import logging

from datetime import datetime

##CONST
SEC_HOUR = 3600.0

whours = [0.0 for i in range(24)]
last = {'watts':0, 'hour':0, 'sech':0}

def calWreg(r, l):
     if r['hour']==l['hour']:
         seg = r['sech'] - l['sech']
         wh = seg * (float(l['watts'])/SEC_HOUR)
         whours[r['hour']]+=wh
     else:
         # watts for previous hour
         lend = {'watts':l['watts'], 'hour':l['hour'], 'sech':SEC_HOUR-1}
         calWreg(lend, l)
         # watts for current reg hour
         rstart = {'watts':l['watts'], 'hour':r['hour'], 'sech':0}
         calWreg(r, rstart)
         # if any hour between hours, mark to -1 previous hour (or put lwatts?)
         if (r['hour']-l['hour']>1):
             whours[r['hour']-1]=-1

def main(argv):
    global last
    inputfile = ''
    if len(argv)!=1:
        print 'Need a file.'
        exit(1)
    inputfile = argv[0]
    print 'Input file is ', inputfile

    with open(inputfile) as fp:
        for line in fp:
            #print line[:-1]
            flds = line.split()
            dt = flds[2]
            m = int(dt[10:12])
            s = int(dt[12:])
            reg = {'watts':int(flds[1]), 'hour':int(dt[8:10]), 'sech':m*60+s}
            calWreg(reg, last)
            last = reg
	
            print str(reg)

    #get date
    print str(whours)
    text_file = open(inputfile + ".hours", "a")
    
    j=0
    for i in whours:
        print j, "%.2f"%i
        text_file.write("%d %.2f\n" % (j,i)) 
        j+=1

    text_file.close()
    print "Sum day Watts: ", "%.2f"%sum(whours)

if __name__ == "__main__":
    main(sys.argv[1:])
