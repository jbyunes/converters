from datetime import datetime

INFILE="scores.txt"
OUTFILE="fromScore.TextGrid"

def to_milliseconds(t):
    h = int(t[0:2])
    m = int(t[3:5])
    s = int(t[6:8])
    ms = int(t[9:])
    return ((h*60+m)*60+s)+(ms/1000)

factor = 1000
data=[]
last_was_bracket = False
with open(INFILE, 'r', encoding='utf-8') as infile:
    for line in infile:
        d = line.split("\t")
        word = d[0].strip()
        start_time = int(d[2])
        stop_time = int(d[3])
        if word[0]=="[": 
            print(f"{word} corrected {start_time} {stop_time} to {start_time} {stop_time+1}")
            word = " "
            last_was_bracket = True
            stop_time = start_time+1
            last_stop_time = stop_time
        else:
            if last_was_bracket:
                if int(last_stop_time) > start_time:
                    print(f"{word} corrected {start_time} {stop_time} to {last_stop_time} {stop_time}")
                    start_time = last_stop_time
            last_was_bracket = False
        data.append((word,start_time,stop_time))

print(f"{len(data)} entries found")

time_factor = 100

x_min = data[0][1]/time_factor
x_max = data[-1][2]/time_factor

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
        outfile.write(f"       intervals [{idx+1}]:\n")
        outfile.write(f"           xmin = {d[1]/time_factor}\n")
        outfile.write(f"           xmax = {d[2]/time_factor}\n")
        outfile.write(f"           text = \"{d[0]}\"\n")

print("ok")
