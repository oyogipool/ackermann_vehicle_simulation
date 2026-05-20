import re

with open('obstacleFieldExp.sdf', 'r') as fp:
    lines = fp.readlines()
    for row_idx, row in enumerate(lines):
        m = re.search("<static>false</static>.*", row)
        if m:
            #print(row[m.start():m.end()])
            print(lines[row_idx])
            lines.pop(row_idx)
        
with open('obstacleFieldExp.sdf', 'w') as fp:
    fp.writelines(lines)  
