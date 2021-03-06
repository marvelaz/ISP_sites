import json, mpu
import re

with open('sites_latest.json') as json_file:
    sites = json.load(json_file)

with open('file2.json') as json_file1:
    data = json.load(json_file1)

with open('adapters_latest.json') as json_file2:
    adapters = json.load(json_file2)

export_data = dict()
final_data = dict()
max_distance = set()
dist = set()
f11 = 0

#get (lat,lon) for siteA
for d in data:
    Router = d['RA']
    for a in adapters[0]['routers']:
        if Router == a['host']:
            export_data.setdefault(Router, {})['Site'] = a['site']
            for s in sites:
                if a['site'] == s['name']:
                    lat1 = s['latitude']
                    lon1 = s['longitude']
                    export_data.setdefault(Router, {})['lat'] = s['latitude']
                    export_data.setdefault(Router, {})['long'] = s['longitude']

#get (lat,lon) for siteB
for d in data:
    Router = d['RB']
    for a in adapters[0]['routers']:
        if Router == a['host']:
            export_data.setdefault(Router, {})['Site'] = a['site']
            for s in sites:
                if a['site'] == s['name']:
                    lat2 = s['latitude']
                    lon2 = s['longitude']
                    export_data.setdefault(Router, {})['lat'] = s['latitude']
                    export_data.setdefault(Router, {})['long'] = s['longitude']

#export siteA and SiteB details to json
with open("export_data.json", 'w') as outfile:
    json.dump(export_data, outfile)

#calc distance for each link
for d in data:
    if d['RA'] == '' or d['RB'] == '':
        continue
    else:
        dist = set()
        distnfo5 = set()
        distnfo10 = set()
        distnfo80 = set()
        Router1 = d['RA']
        Router2 = d['RB']
        lat1 = export_data[Router1]['lat']
        lon1 = export_data[Router1]['long']
        lat2 = export_data[Router2]['lat']
        lon2 = export_data[Router2]['long']

        d1 = mpu.haversine_distance((lat1, lon1), (lat2, lon2))
        title = 'From: ' + Router1 + ' to: ' + Router2
        final_data.setdefault(title, {})['link_distance'] = d1
        final_data.setdefault(title, {})['SiteA'] = d['Site1']
        final_data.setdefault(title, {})['Provider'] = d['provider']
        for s in sites:
            latn = s['latitude']
            lonn = s['longitude']
            f = mpu.haversine_distance((lat1, lon1), (latn, lonn))

            if f < d1: #Sites in 5 km range
                if f == 0:
                    continue
                else:
                    name1 = 'to: ' + s['name']
                    dist.update(dict({name1: f}).items())
            else:
                continue

            final_data.setdefault(title, {})['nearest site'] = dict(sorted(dist, key=lambda tup: tup[1])[:4])

# find NFO nearest site
        for s in sites:
            m = re.search('NFO-\d+', s['name'])
            if m is None:
                continue
            else:
                latn = s['latitude']
                lonn = s['longitude']
                f11 = mpu.haversine_distance((lat1, lon1), (latn, lonn))
                if f11 <= 5:
                   name2 = 'to: ' + s['name']
                   distnfo5.update(dict({name2: f11}).items())
                   #final_data.setdefault(title, {})['nearest NFO site'] = dict(sorted(distnfo, key=lambda tup: tup[1])[:2])
                elif f11 <10:
                    name2 = 'to: ' + s['name']
                    distnfo10.update(dict({name2: f11}).items())
                elif f11 <= 80:
                    name2 = 'to: ' + s['name']
                    distnfo80.update(dict({name2: f11}).items())
                else:
                    continue

        if len(distnfo5) > 0:
            final_data.setdefault(title, {})['NFO site < 5km'] = dict(sorted(distnfo5, key=lambda tup: tup[1])[:2])
        elif len(distnfo10) > 0:
            final_data.setdefault(title, {})['NFO site < 10km'] = dict(sorted(distnfo10, key=lambda tup: tup[1])[:2])
        elif len(distnfo80) > 0:
            final_data.setdefault(title, {})['NFO site < 80km'] = dict(sorted(distnfo80, key=lambda tup: tup[1])[:2])
        else:
            final_data.setdefault(title, {})['nearest NFO site'] = 'OUT OF RANGE'

with open("final_datav1.json", 'w') as outfile:
    json.dump(final_data, outfile, indent=4)




