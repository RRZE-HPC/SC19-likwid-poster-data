#!/usr/bin/env python3

import sys, re


if len(sys.argv) != 2:
    print("Filename required")
    sys.exit(1)

filename = sys.argv[1]
outfile = filename.replace(".raw", ".dat")


ofp = open(outfile, "w")

with open(filename, "r") as fp:
    values = []
    names = []
    size = None
    iters = None
    threads = None
    first = True
    for l in fp.read().split("\n"):
        if l.startswith("#########################"):
            #print())

            if len(values) > 0:
                print(names)
                print(values)
                if first:
                    ofp.write("# Size(B) " + " ".join([str(v) for v in names]) + "\n")
                    first = False
                ofp.write(" ".join([str(size*1E3)] + [str(v) for v in values]) + "\n")
                values = []
                names = []
                iters = None
                size = None
                threads = None
            size = int(l.replace("#",""))
        elif l.startswith("Using") and "threads" in l:
            llist = re.split(" ", l)
            threads = int(llist[1])
            names.append("Threads")
            values.append(threads)
        elif l.startswith("Iterations") and not "per" in l:
            key, val = re.split(":\s+", l)
            iters = int(val)
        elif l.startswith("Inner loop executions"):
            key, val = re.split(":\s+", l)
            iters *= int(val)
        elif l.startswith("MByte/s:"):
            key, val = re.split(":\s+", l)
            names.append("Bandwidth(MByte/s)")
            values.append(float(val))
        elif l.startswith("Data volume (Byte)"):
            key, val = re.split(":\s+", l)
            #print(val)

            names.append("DataVolume(B)")
            values.append(int(val))
            if iters:
                names.append("Iterations")
                values.append(iters)
                names.append("DataVolume(B)/Iterations")
                values.append(float(val)/iters)
        elif "data volume" in l and "STAT" in l:
            llist = l.split(",")
            if "read" in llist[0]:
                name = "MeasuredReadDataVolume(B)"
            elif "write" in llist[0]:
                name = "MeasuredWriteDataVolume(B)"
            else:
                name = "MeasuredTotalDataVolume(B)"
            val = llist[1]
            values.append((float(val)*1E9))
            names.append(name)
            name += "/Iterations"
            #name, val, nothing = l.split(",")
            values.append((float(val)/iters)*1E9)
            names.append(name)
        elif "Memory bandwidth" in l and "STAT" in l:
            llist = l.split(",")
            name = "MeasuredBandwidth(MBytes/s)"
            val = llist[1]
            values.append((float(val)))
            names.append(name)

ofp.close()
