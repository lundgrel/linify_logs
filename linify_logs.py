
from distutils.fancy_getopt import FancyGetopt
from math import fabs
import os
from pickle import FALSE
import re
import sys
from xmlrpc.client import boolean


re_start = re.compile('^\d\d\:\d\d\:\d\d\.\d\d\d\ \{\d+\} \[\d+\] \|')

if len(sys.argv) < 2:
    print("linify_logs inputfile.log [output.filename]")
    exit(0)

infile = sys.argv[1]
outfile = ''
if len(sys.argv) == 2:
    (base, ext) = os.path.splitext(infile)
    outfile = base + '-oneline' + ext
else:
    outfile = sys.argv[2]
   
print('output to ' + outfile)

buf : str = None
with open(infile, 'r') as in_f:
    with open(outfile, 'w') as out_f:
        count = 0

        def add_buf(l: str):
            global buf
            if buf is None:
                buf = l
            else:
                buf = buf.rstrip() + '\\n' + l

        def write_buf():
            global buf
            if buf:
                out_f.write(buf)
                buf = None

        while True:
            count += 1

            line = in_f.readline()
            if not line: break;


            if line.find('sending request to sip:172.24.14.13:5060;transport=TCP;lr') > 0:
                bp=17

            match_start = re_start.match(line)

            if match_start:
                write_buf()

            add_buf(line)


        # end of loop. write out cache
        write_buf()



