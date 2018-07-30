import mpu, math

# Point one
lat1 = 52.2296756
lon1 = 21.0122287

# Point two
lat2 = 52.406374
lon2 = 16.9251681

origin = lat1, lon1
destination = lat2, lon2
radius = 6371

# What you were looking for
dist = mpu.haversine_distance((lat1, lon1), (lat2, lon2))

dlat = math.radians(lat2 - lat1)
dlon = math.radians(lon2 - lon1)
a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
d = radius * c

print("distancia usando el metodo mpu")
print(dist)
print("distancia usando el metodo math")
print(d)
print(d==dist)
print(origin)
print(destination)