import math

tar_nonrely = -150
tar_nonrelx = -150
nonrelx = 0
nonrely = 0

print str(math.degrees(math.atan(float(tar_nonrely-nonrely)/float(tar_nonrelx-nonrelx))))

if nonrelx < tar_nonrelx:
	if nonrely < tar_nonrely:
		quadrant = 1
	else:
		quadrant = 4
else:
	if nonrely < tar_nonrely:
		quadrant = 2
	else:
		quadrant = 3

angle =  math.degrees(math.atan(float(tar_nonrely-nonrely)/float(tar_nonrelx-nonrelx)))
if quadrant == 4:
	angle += 270
elif quadrant == 3:
	angle += 180
elif quadrant == 2:
	angle += 90

print angle
#print str(angle)
#print str(math.degrees(math.atan(float(tar_nonrely-nonrely)/float(tar_nonrelx-nonrelx))))

x = raw_input(' SSS')
