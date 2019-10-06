'''
Aaron Brown
Aug 13, 2019
Fourier analysis in complex plane

Use sum of rotating vectors to create
any arbitary coninous differentiable boundary
'''

import matplotlib
from collections import deque
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
# Can set limits for graph here
ax = plt.axes(xlim=(-3, 3), ylim=(-3, 3))
pathLength = 100
xdata1, ydata1 = deque(maxlen=pathLength), deque(maxlen=pathLength)
xdata2, ydata2 = deque(maxlen=pathLength), deque(maxlen=pathLength)
from funcFourier import *
import math
PI = np.pi

''' 
Boundary function
input:
	0 - step function
	1 - polygon function
	2 - custom
'''

numFourier = 14

# fourier series 
# Resolution for drawing boundary
def createFourier(numVectors):
	vectors = []

	boundary = boundaryFunction(1)
	
	for n in range(-numVectors,numVectors+1):
		cn =  toE(integrate(boundary, [1,0,-2*PI*n],0,1,0.01))
		#print(cn)
		vectors.append(multipleE(cn,[1,0,n*2*PI]))
	
	'''
	offset = 0;
	for vector in vectors:
		vector[1] += offset
	'''
	'''
	temp = vectors[0]
	vectors[0] = vectors[len(vectors)/2]
	vectors[len(vectors)/2] = temp
	'''
	return vectors

vectors1 = [[0.0035144853346719958, 1.5054570151515678e-14, -87.96459430051421], [8.74904580178788e-05, 3.965514675034194e-14, -81.68140899333463], [0.00011821077861863104, 3.7420825033324577e-13, -75.39822368615503], [0.0056772812756372215, -1.3902766892254353e-14, -69.11503837897544], [8.986714366644895e-05, -2.5094160410172073e-13, -62.83185307179586], [0.0001128781434676946, -1.4676542939705438e-12, -56.548667764616276], [0.010711253718336337, 7.611807685158019e-15, -50.26548245743669], [9.252703659995073e-05, -1.3217542628662335e-12, -43.982297150257104], [0.00010810689369175272, -6.057505583764661e-13, -37.69911184307752], [0.027381733297182506, -2.3123958657382955e-15, -31.41592653589793], [9.54979972708804e-05, -1.0717364552925566e-12, -25.132741228718345], [0.00010383244307021061, 2.338973055584681e-13, -18.84955592153876], [0.1710044995898432, -1.1970291463454638e-15, -12.566370614359172], [9.881247110490529e-05, 6.616309689438626e-13, -6.283185307179586], [0.00010000000000002195, 4.114547244581586e-13, 0.0], [0.683942990134101, 6.428079347032577e-17, 6.283185307179586], [0.00010250830754674096, -4.177806349368314e-13, 12.566370614359172], [9.6562904615358e-05, -2.851895900483494e-13, 18.84955592153876], [0.042769883124536924, -8.010493868028985e-16, 25.132741228718345], [0.00010662976665772213, 8.581718428730113e-13, 31.41592653589793], [9.348129299742262e-05, 8.25782273712199e-13, 37.69911184307752], [0.013982536881735947, 4.621368069805771e-15, 43.982297150257104], [0.00011122876252543483, 1.9494996579460794e-12, 50.26548245743669], [9.07210177723012e-05, 2.935152846617866e-12, 56.548667764616276], [0.006864234822582756, -8.46609096967886e-15, 62.83185307179586], [0.00011636640799344948, 4.0995418189798905e-13, 69.11503837897544], [8.825277125448089e-05, -1.1204094412577167e-12, 75.39822368615503], [0.004071944947305993, -3.3868462890540315e-14, 81.68140899333463], [0.00012211494585961935, -1.5839311577287786e-12, 87.96459430051421]]

vectors2 = createFourier(numFourier)


'''
vectors1 = []
for i in range(2*numFourier+1):
	vectors1.append([0.0, 0.0, vectors2[i][2]])
	#vectors1.append([0.0, vectors2[i][1], vectors2[i][2]])

vectors1[15][0] = 1.0
vectors1[15][1] = 0
'''

mag_cos = 0
mag_sin = 0
target = 0
for i in range(len(vectors1)):
	mag_cos += 2*vectors1[i][0]*vectors2[i][0]*np.cos(vectors1[i][1]-vectors2[2][1])
	mag_sin += 2*vectors1[i][0]*vectors2[i][0]*np.sin(vectors1[i][1]-vectors2[2][1])
	target += vectors1[i][0]*vectors1[i][0]+vectors2[i][0]*vectors2[i][0]

mag = np.sqrt(mag_cos*mag_cos+mag_sin*mag_sin)
theta = np.arctan2(mag_sin,mag_cos)

print("curr mag ",mag)
print("target ",target)
print("curr angle ",theta)
target_angle = np.arccos(target/mag)

print("target angle ",target_angle)

print("calc area ",calculateArea(vectors2))

Area = 0
for i, vector in enumerate(vectors2):
	Area += vector[0]*vector[0]
Area *= PI

print("square area: ",Area)


lines = []
for i in range(len(vectors1)+1+len(vectors2)+1):
#for i in range(len(vectors1)+1):
	lobj = ax.plot([],[])[0]
	lines.append(lobj)

def init():
	for line in lines:
		line.set_data([],[])
	return lines

prev_vector = vectors1

#visu_type
# 0 : time signal
# 1 : contour 
# 2 : snow flake
# 3 : radian time
visu_type = 3
transform = False
def update(t):
	global lines
	global prev_vector

	if(visu_type == 0):
		vec1 = [0,0]
		for i, vector in enumerate(vectors2):
			f = calcE(vector,t)
			lines[i].set_data([vec1[0],f[0]+vec1[0]],[vec1[1],f[1]+vec1[1]])
			vec1[0] += f[0]
			vec1[1] += f[1]
		xdata1.append(vec1[0])
		ydata1.append(vec1[1])
		lines[-1].set_data(xdata1, ydata1)
	elif(visu_type == 1):
		for dt in np.linspace(0, 1, 100):
			vec1 = [0,0]
			for i, vector in enumerate(vectors2):
				f = calcE(vector,dt)
				vec1[0] += f[0]
				vec1[1] += f[1]
			xdata1.append(vec1[0])
			ydata1.append(vec1[1])
		lines[0].set_data(xdata1, ydata1)
	elif(visu_type == 2):
		for i, vector in enumerate(vectors1):
			f = calcE(vector,0)
			lines[i].set_data([[0,f[0]],[0,f[1]]])
	elif(visu_type == 3):
		
		for dt in np.linspace(0, 2*PI, 100):
			
			vec1 = [0,0]
			for i, vector in enumerate(vectors2):
				f = calcE(vector,dt/(2*PI))
				vec1[0] += f[0]
				vec1[1] += f[1]
			mag = np.sqrt(vec1[0]*vec1[0]+vec1[1]*vec1[1])
			
			'''
			mag = 0
			if dt >= 0 and dt < PI/4:
				mag += 1/np.cos(dt)
			elif dt >= PI/4 and dt < 3*PI/4:
				mag += 1/np.sin(dt)
			elif dt >= 3*PI/4 and dt < 5*PI/4:
				mag += -1/np.cos(dt)
			elif dt >= 5*PI/4 and dt < 7*PI/4:
				mag += 1/np.sin(-dt)
			else:
				mag += 1/np.cos(dt)
			'''
			xdata1.append(mag*np.cos(dt))
			ydata1.append(mag*np.sin(dt))
		lines[0].set_data(xdata1, ydata1)

	if(transform):
		ray_res = 0.005
		angle_res = 0.1
		total_diff = 0
		for i, vector in enumerate(vectors1):
				diff = vectors2[i][n]-vectors1[i][n]
				if(n==0):
					delta = max(min(diff, ray_res), -ray_res)
				else:
					delta = max(min(diff, angle_res), -angle_res)
				vectors1[i][n] += delta
	
	#print("2 ",vectors1)
	
	for dt in np.linspace(0, 1, 100):
		vec2 = [0,0]
		for i, vector in enumerate(vectors2):
			f = calcE(vector,dt)
			vec2[0] += f[0]
			vec2[1] += f[1]
		xdata2.append(vec2[0])
		ydata2.append(vec2[1])
	lines[-1].set_data(xdata2, ydata2)
	

	'''
	for vector in vectors:
		vector[1]+=0.002
	'''


	'''
	if(t%100==0):
		newVectors = createFourier()
		for i in range(len(vectors)):
			vectors[i] = newVectors[i]
	'''
	return lines
	

ani = FuncAnimation(fig, update, frames=np.linspace(0, 1, 100), interval=40,
                    init_func=init, blit=True)

plt.show()