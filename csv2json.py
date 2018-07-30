import csv
import json


csvfile = open('links_v1.csv', 'r', encoding='utf-8')

jsonfile = open('file2.json', 'w')

fieldnames = ("Site1", "RA", "portA", "Site2", "RB", "portB", "BW", "provider")

reader = csv.DictReader(csvfile, fieldnames)

for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')