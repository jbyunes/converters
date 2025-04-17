from datetime import datetime

INFILE="sample.srt"
OUTFILE="out.TextGrid"

def to_milliseconds(t):
    h = int(t[0:2])
    m = int(t[3:5])
    s = int(t[6:8])
    ms = int(t[9:])
    return ((h*60+m)*60+s)+(ms/1000)

data=[]
with open(INFILE, 'r', encoding='utf-8') as infile:
    while True:
        number = infile.readline()
        if number == "":
            break
        number = int(number)
        timecodes = infile.readline().strip()
        start_time = to_milliseconds(timecodes[0:12])
        end_time = to_milliseconds(timecodes[17:29])
        text = infile.readline().strip()
        infile.readline() # read blank line
        data.append((number,start_time,end_time,text))

x_min = data[0][1]
x_max = data[-1][2]

with open(OUTFILE, 'w', encoding='utf-8') as outfile:
    outfile.write("File type = \"ooTextFile\"\n")
    outfile.write("Object class = \"TextGrid\"\n")
    outfile.write("\n")
    outfile.write(f"xmin = {x_min}\n")
    outfile.write(f"xmax = {x_max}\n")
    outfile.write("tiers? <exists>\n")
    outfile.write("size = 1\n")
    outfile.write("item []:\n")
    outfile.write("    item [1]:\n");
    outfile.write("       class = \"IntervalTier\"\n")
    outfile.write("       name = \"words\"\n")
    outfile.write(f"       xmin = {x_min}\n") 
    outfile.write(f"       xmax = {x_max}\n");
    outfile.write(f"       intervals: size = {len(data)}\n");
    for idx,d in enumerate(data):
        outfile.write(f"       intervals [{d[0]}]:\n")
        outfile.write(f"           xmin = {d[1]}\n")
        outfile.write(f"           xmax = {d[2]}\n")
        outfile.write(f"           text = \"{d[3]}\"\n")

print("ok")
