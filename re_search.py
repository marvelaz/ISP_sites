import re
import json

with open('sites_latest.json') as json_file:
    sites = json.load(json_file)

i = 0
j = 0
for s in sites:
    m = re.search('NFO-\d+', s['name'])
    if m is None:
        j += 1
        continue
    else:
        print(m.group(0))
        i += 1

print(i)
print(j)