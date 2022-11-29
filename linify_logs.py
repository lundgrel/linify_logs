
import os
import re
import sys


re_start_ms = '^\d\d\:\d\d\:\d\d\.\d\d\d\ \{\d+\} \[\d+\] \|\;\;'
re_start_tas = '^\d\d\:\d\d\:\d\d\.\d\d\d\ \{\d+\} \[\d+\] \|[^|]*\|'

re_end_ms = '\|.+\,\d+$'
re_end_tas='\|\|.*\|\d+$'

re_s = [ (re.compile(re_start_ms), re.compile(re_end_ms)), (re.compile(re_start_tas), re.compile(re_end_tas))]

used_re = ()

if len(sys.argv) == 0:
    print("linify_logs inputfile.log [output.filename]")
    exit(0)

infile = sys.argv[0]
outfile = ''
if len(sys.argv) == 1:
    (base, ext) = os.path.splitext(infile)
    outfile = base + '-oneline' + ext
else:
    outfile = sys.argv[1]
   
print('output to ' + outfile)

with open(infile, 'r') as in_f:
    with open(outfile, 'w') as out_f:




        in_log = False
        count = 0

        def write_line(l: str):
            if in_log:
                outfile.write(l.chomp())
                outfile.write('\n')
            else:
                outfile.write(l)

        while True:
            count += 1

            line = in_f.readline()
            if not line: break;

            
            if len(used_re) == 0:
                for (re_start, re_end) in re_s:
                    if re_start.match(line) is not None:
                        used_re = (re_start, re_end)
                        break;
                # if line doesn't match anything (like log-headers)
                if len(used_re) == 0:
                    write_line(line)
                    in_log = False
                    continue;

            match_end = used_re[1].match(line)

            if match_end is not None:
                write_line(line)
                in_log = False
                continue;

            match_start = used_re[0].match(line)

            if match_start is None: # non-log line.
                out_f.write(line)
                in_log = True
                continue;






