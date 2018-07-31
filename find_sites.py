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
        distnfo = set()
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
                    #final_data.setdefault(title, {}).setdefault('distance',{})[name1] = f
                    dist.update(dict({name1: f}).items())
            else:
                continue

            final_data.setdefault(title, {})['nearest site'] = dict(sorted(dist, key=lambda tup: tup[1])[:3])
            #final_data.setdefault(title, {})['nearest site'] = min(final_data[title]['distance'], key=final_data[title]['distance'].get)
            #sorted(dist, key=lambda tup: tup[1])

# find NFO nearest site
        for s in sites:
            m = re.search('NFO-\d+', s['name'])
            if m is None:
                continue
            else:
                latn = s['latitude']
                lonn = s['longitude']
                f11 = mpu.haversine_distance((lat1, lon1), (latn, lonn))
                if f11 <= 100:
                   name2 = 'to: ' + s['name']
                   #final_data.setdefault(title, {}).setdefault('FO distance', {})[name2] = f11
                   distnfo.update(dict({name2: f11}).items())

                   #final_data.setdefault(title, {})['nearest NFO site'] = min(final_data[title]['FO distance'], key=final_data[title]['FO distance'].get)
                   final_data.setdefault(title, {})['nearest NFO site'] = dict(sorted(distnfo, key=lambda tup: tup[1])[:2])
                else:
                   final_data.setdefault(title, {})['nearest NFO site'] = 'OUT OF RANGE'




with open("final_datav1.json", 'w') as outfile:
    json.dump(final_data, outfile, indent=4)




