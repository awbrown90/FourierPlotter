'''
Aaron Brown
Aug 13, 2019
Fourier analysis in complex plane

Use sum of rotating vectors to create
any arbitary coninous differentiable boundary
'''

import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
# Can set limits for graph here
ax = plt.axes(xlim=(-3, 3), ylim=(-3, 3))
xdata, ydata = [], []
from funcFourier import *

''' 
Boundary function
input:
	0 - step function
	1 - polygon function
	2 - custom
'''
boundary = boundaryFunction(1)

vectors = []
# fourier series 
# Resolution for drawing boundary
numFourier = 50
for n in range(-numFourier,numFourier+1):
	cn =  toE(integrate(boundary, [1,0,-2*PI*n],0,1,0.01))
	vectors.append(multipleE(cn,[1,0,n*2*PI]))

lines = []
for i in range(len(vectors)+1):
	lobj = ax.plot([],[])[0]
	lines.append(lobj)

def init():
	for line in lines:
		line.set_data([],[])
	return lines

def update(t):
	global lines
	vec = [0,0]
	for i, vector in enumerate(vectors):
		f = calcE(vector,t)
		lines[i].set_data([vec[0],f[0]+vec[0]],[vec[1],f[1]+vec[1]])
		vec[0] += f[0]
		vec[1] += f[1]
	xdata.append(vec[0])
	ydata.append(vec[1])

	lines[-1].set_data(xdata, ydata)

	return lines
	

ani = FuncAnimation(fig, update, frames=np.linspace(0, 1, 100),
                    init_func=init, blit=True)

plt.show()