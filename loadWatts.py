import sys

import requests

urlroot='http://localhost:8080/reg/'
header={'Accept': 'text/text'}

def main(argv):
    if len(argv)!=1:
        print "Use: loadWatts.py file"
        exit(1)
    
    inputfile = argv[0]
    print 'Input file is ', inputfile

    with open(inputfile) as fp:
        for line in fp:
            vals = line[:-1].split(' ')
            print str(vals)
            url=urlroot+'?w='+vals[1]+'&d='+vals[2]
            print url
            r = requests.get(url, headers=header)

if __name__ == "__main__":
    main(sys.argv[1:])
