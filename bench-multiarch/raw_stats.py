#!/usr/bin/env python3

import sys, re, os, os.path, glob

# Scale values to include write-allocate/read-for-ownership
scales = { "load" : 1.0 ,
           "store" : 2.0,
           "copy" : 1.5,
           "stream" : 1.333,
           "triad" : 1.25}


def stats(inlist):
    mini = 100000000000000000
    maxi = 0
    s = 0
    d = []
    for l in inlist:
        f = float(l)
        d.append(f)
    mini = min(d)
    maxi = max(d)
    s = sum(d)
    sd = sorted(d)
    medi = sd[int(len(sd)/2)]

    return mini, maxi, s/len(d), medi

def read_file(fname, column):
    fp = open(fname)
    inp = fp.read().split("\n")
    fp.close()
    out = []
    for l in inp:
        if l.startswith("#") or not l.strip(): continue
        llist = re.split("\s+", l)
        if len(llist) >= column:
            out.append(float(llist[column]))
    return out

if len(sys.argv) < 2:
    print("Hostname and column index required")
    sys.exit(1)

hostname = sys.argv[1]
if not os.path.exists(hostname):
    print("Folder for hostname {} does not exist".format(hostname))
    sys.exit(1)

columns = sys.argv[2:]
for i,c in enumerate(columns):
    try:
        columns[i] = int(c)
    except:
        print("Column argument {} must be a number (column index)".format(c))
        sys.exit(1)

for f in glob.glob(os.path.join(hostname, "*.dat")):
    name = None
    for m in scales:
        if m in f:
            name = m
    data = read_file(f, columns[0])
    mini, maxi, mean, medi = stats(data)
    #maxi = maxi*scales[name]
    out = [f, str(maxi).replace(".", ",")]
    if len(columns) > 1:
        for c in columns[1:]:
            data = read_file(f, c)
            mini, maxi, mean, medi = stats(data)
            out.append(str(maxi).replace(".", ","))
    print(" ".join(out))

#print("%.2f %.2f %.2f %.2f" % (mini, maxi, mean, medi))
