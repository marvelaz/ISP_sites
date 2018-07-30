import json, mpu

with open('sites_latest.json') as json_file:
    data = json.load(json_file)


lat1 = 22.88328708
lon1 = -102.29083059
distance = {}

km = 60
max_distance =[]

total = []

for p in data:

    lat2 = p['latitude']
    lon2 = p['longitude']
    d = mpu.haversine_distance((lat1, lon1), (lat2, lon2))
    max_distance.append(d)
    distance.setdefault('Router1', {})['Lat'] = lat2
    distance.setdefault('Router1', {})['Long'] = lon2
    if d <= km:
        name = 'to: ' + p['name']
        distance.setdefault('Router1', {})[name] = d
    distance.setdefault('Router1', {})['Min_distance'] = min(max_distance)
print(distance)
