import re

with open('obstacleFieldExp.sdf', 'r') as fp:
    lines = fp.readlines()
    row_idx = 1
    for row in lines:
        m = re.search("<model name=.*>", row)
        if m:
            print(row[m.start():m.end()])
            lines.insert(row_idx, "      <static>true</static>\n")
            print(lines[row_idx])
        row_idx += 1
        
with open('obstacleFieldExp.sdf', 'w') as fp:
    fp.writelines(lines)  
