'''
Aaron Brown
Aug 13, 2019
Fourier analysis in complex plane

Define functions for drawFourier.py
'''
import numpy as np
import math
PI = np.pi

'''
Multiply two rotating vectors
input: two rotating vectors in the form  A*e^(B*x+C)i, [A, B, C]
output: product as a new rotating vector
'''
def multipleE(e1,e2):
	return [e1[0]*e2[0], e1[1]+e2[1], e1[2]+e2[2]]

'''
Convert rotating vector to complex number, (A*cos(x), B*i*sin(x))
input: rotating vector and time
output: real, imaginary components
'''
def calcE(e1,t):
	return e1[0]*np.cos(e1[1]+e1[2]*t), e1[0]*np.sin(e1[1]+e1[2]*t)

'''
Convert complex number to rotating vector
input: real, imaginary components, [r, i]
output: rotating vector in the form A*e^(B*x+C)i, [A, B, C]
'''
def toE(ri):
	r = ri[0]
	i = ri[1]
	return [np.sqrt(r*r+i*i), math.atan2(i,r), 0]

'''
Integrate over function using numerical integration 
from start to stop range in dt increments

input: 
	function(t), defines the boundary to draw
	en, rotating vector to multiply function by
	start, beginning of range
	stop, end of range
	dt, resolution of integration
output: complex number in form [r, i]
'''
def integrate(func, en, start, stop, dt):
	sumR = 0
	sumI = 0
	for t in np.arange(start,stop,dt):
		fe = toE(func(t))
		f = multipleE(fe, en)
		r,i = calcE(f, t)
		r *= dt
		i *= dt
		sumR += r
		sumI += i
	return [sumR, sumI]

'''
Step function, 
goes from 1 from [0, 0.5] then -1 over [0.5, 1] 
input: time between [0, 1]
output: either 1 or -1 based on time
'''
def stepFunction(t):
	if t < 0:
		t *= -1
	if t > 1:
		t -= int(t)
	if t < 0.5:
		return [1, 0]
	else:
		return [-1, 0]

'''
Define points for polygon incribed in circle of radius r
input: 
	s, number of sides
	cx, x center
	cy, y center
	r, radius
	theta, start angle
output: points of the polygon, E.G. a square would output 4 points
'''
def polygonGenerator(s, cx, cy, r, theta):
	points = []
	sector = (2*PI)/s
	for i in range(s):
		x, y = calcE([r, theta, sector],i)
		points.append([x,y])
	return points

'''
Draw polygon as function of time
interpolates points between polygon points

input: time between [0, 1]
output: interpolated points of polygon
'''
def polygonFunction(t):
	# Define polygon here by setting polygonGenerator variables, see above for details
	polyPoints = polygonGenerator(3, 0, 0 , 1, PI/2)
	span = 1./len(polyPoints)

	if t < 0:
		t *= -1
	if t >= 1:
		t -= int(t)
	index = int(t/span)
	vector = [polyPoints[(index+1)%len(polyPoints)][0]-polyPoints[index][0], polyPoints[(index+1)%len(polyPoints)][1]-polyPoints[index][1]]
	mag = np.sqrt(vector[0]*vector[0]+vector[1]*vector[1])
	vector = [vector[0]/span, vector[1]/span]
	split = t-index*span
	return [vector[0]*split+polyPoints[index][0], vector[1]*split+polyPoints[index][1]]

'''
Custom boundary function
input: time between [0, 1]
output: you decide
'''
def custom(t):
	if t < 0:
		t *= -1
	if t > 1:
		t -= int(t)

	# Define this function returning some complex value, right now just returning 1 + i 
	return [1, 1]

'''
Pick different kinds of boundaries
either classic step function, polygons, or custom
input: 
	0, step function
	1, polygon, can define polygon in polygonFunction
	2 or other, custom, can define custom in custom function
output: boundary function(t)
'''
def boundaryFunction(choice):

	#use step function
	if choice == 0:
		return stepFunction
	if choice == 1:
		return polygonFunction
	else:
		return custom



