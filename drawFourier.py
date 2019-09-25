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
		vectors.append(multipleE(cn,[1,0,n*2*PI]))
	
	offset = 0;
	for vector in vectors:
		vector[1] += offset
	'''
	temp = vectors[0]
	vectors[0] = vectors[len(vectors)/2]
	vectors[len(vectors)/2] = temp
	'''
	return vectors

vectors2 = createFourier(numFourier)

vectors1 = []
for i in range(2*numFourier+1):
	vectors1.append([0.0, vectors2[i][1], vectors2[i][2]])

vectors1[15][0] = 1.0


#print(calculateArea(vectors1))

lines = []
#for i in range(len(vectors1)+1+len(vectors2)+1):
for i in range(len(vectors1)+1):
	lobj = ax.plot([],[])[0]
	lines.append(lobj)

def init():
	for line in lines:
		line.set_data([],[])
	return lines

prev_vector = vectors1

def update(t):
	global lines
	global prev_vector

	'''
	vec1 = [0,0]
	for i, vector in enumerate(vectors1):
		f = calcE(vector,t)
		lines[i].set_data([vec1[0],f[0]+vec1[0]],[vec1[1],f[1]+vec1[1]])
		vec1[0] += f[0]
		vec1[1] += f[1]
	xdata1.append(vec1[0])
	ydata1.append(vec1[1])
	lines[-1].set_data(xdata1, ydata1)
	'''

	for dt in np.linspace(0, 1, 100):
		vec1 = [0,0]
		for i, vector in enumerate(vectors1):
			f = calcE(vector,dt)
			vec1[0] += f[0]
			vec1[1] += f[1]
		xdata1.append(vec1[0])
		ydata1.append(vec1[1])
	lines[0].set_data(xdata1, ydata1)

	#print("1 ",vectors1)

	res = 0.01
	total_diff = 0
	for i, vector in enumerate(vectors1):
		diff = vectors2[i][0]-vectors1[i][0]
		delta = max(min(diff, res), -res)
		old = vectors1[i][0]
		vectors1[i][0] += delta
		new = vectors1[i][0]
	
	#print("2 ",vectors1)
	'''
	vec2 = [0,0]
	for i, vector in enumerate(vectors2):
		f = calcE(vector,t)
		lines[i+len(vectors1)].set_data([vec2[0],f[0]+vec2[0]],[vec2[1],f[1]+vec2[1]])
		vec2[0] += f[0]
		vec2[1] += f[1]
	xdata2.append(vec2[0])
	ydata2.append(vec2[1])
	
	lines[-1].set_data(xdata2, ydata2)
	'''

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