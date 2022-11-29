
from distutils.fancy_getopt import FancyGetopt
from math import fabs
import os
from pickle import FALSE
import re
import sys
from xmlrpc.client import boolean


re_start_ms = '^\d\d\:\d\d\:\d\d\.\d\d\d\ \{\d+\} \[\d+\] \|\;\;'
re_start_tas = '^\d\d\:\d\d\:\d\d\.\d\d\d\ \{\d+\} \[\d+\] \|[^|]*\|'


re_s = [ re.compile(re_start_ms), re.compile(re_start_tas) ]

used_re = None

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


        def write_line(l: str, in_log: boolean):
            if in_log:
                out_f.write(l.rstrip())
                out_f.write('\n')
            else:
                out_f.write(l)

        def add_buf(l: str):
            global buf
            if buf is None:
                buf = l
            else:
                buf = buf.rstrip() + '\n' + l

        def write_buf():
            global buf
            if buf:
                write_line(buf, False)
                buf = None

        while True:
            count += 1

            line = in_f.readline()
            if not line: break;

            
            if used_re is None:
                for re_start in re_s:
                    if re_start.match(line) is not None:
                        used_re = re_start
                        break;
                # if line doesn't match anything (like log-headers)
                if used_re is None:
                    write_line(line, False)
                    continue;

            match_start = used_re.match(line)

            if match_start:
                write_buf()

            add_buf(line)


        # end of loop. write out cache
        write_buf()



