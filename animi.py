import numpy as np
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math

fig, ax = plt.subplots()
ax = plt.axes(xlim=(-3, 3), ylim=(-3, 3))
xdata, ydata = [], []
PI = np.pi

# lets integrate e^(2*pi*i*t)*dt from 0 to 1

def multipleE(e1,e2):
	return [e1[0]*e2[0], e1[1]+e2[1], e1[2]+e2[2]]

def calcE(e1,t):
	return e1[0]*np.cos(e1[1]+e1[2]*t), e1[0]*np.sin(e1[1]+e1[2]*t)


def Integrate(f, start, stop, dt):
	sumR = 0
	sumI = 0
	for t in np.arange(start,stop,dt):
		r,i = calcE(f, t)
		r *= dt
		i *= dt
		sumR += r
		sumI += i
	return [sumR, sumI]

def toE(ri):
	r = ri[0]
	i = ri[1]
	return [np.sqrt(r*r+i*i), math.atan2(i,r), 0]

def stepFunction(t):
	if t < 0:
		t *= -1
	if t > 1:
		t -= int(t)
	if t < 0.5:
		return [1, 0]
	else:
		return [-1, 0]

def squareFunction(t,x,y):
	if t < 0:
		t *= -1
	if t > 1:
		t -= int(t)
	if t < 1./8:
		return [1+x, 8*t+y]
	if t < 3./8:
		return [1-2*4*(t-1./8)+x, 1+y] 
	if t < 5./8:
		return [-1+x, 1-2*4*(t-3./8)+y]
	if t < 7./8:
		return [-1+2*4*(t-5./8)+x, -1+y]
	else:
		return [1+x, -1+1*8*(t-7./8)+y]

def polygonGenerator(s, cx, cy, r, theta):
	points = []
	sector = (2*PI)/s
	for i in range(s):
		x, y = calcE([r, theta, sector],i)
		points.append([x,y])
	return points

polyPoints = polygonGenerator(6, 0, 0 , 1, 0)
#polyPoints = [[1, 1], [-1, 1], [-1, -1], [1, -1]]
#polyPoints = [[0, 1], [-1, -1], [1, -1]]
span = 1./len(polyPoints)
def polygonFunction(t):
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

def Integrate2(en, start, stop, dt):
	sumR = 0
	sumI = 0
	for t in np.arange(start,stop,dt):
		#fri = polygonFunction(t)
		fri = stepFunction(t)
		fe = toE(fri)
		f = multipleE(fe, en)
		r,i = calcE(f, t)
		r *= dt
		i *= dt
		sumR += r
		sumI += i
	return [sumR, sumI]


vectors = []

#print("Integration test ", Integrate([1,0,2*PI],0,1,0.01))

'''
numVec = 10
vectors = [[1,0,2*PI]]
for i in range(numVec):
	vectors.append([vectors[i][0]*.5,0,vectors[i][2]*2])
'''


# fourier series 
numFourier = 2
for n in range(-numFourier,numFourier+1):
	#cn =  toE(Integrate(multipleE([1,0,-2*PI*n],[1,0,2*PI]),0,1,0.01))
	cn =  toE(Integrate2([1,0,-2*PI*n],0,1,0.01))
	vectors.append(multipleE(cn,[1,0,n*2*PI]))

lengths = []
for v in vectors:
	length = v[0]
	if length < 0.01:
		length = 0
	lengths.append(length)
print(lengths)



#vectors = [[1,0,2*PI],[0.5,0,4*PI],[0.25,0,8*PI],[0.125,0,7*PI]]

lines = []
for i in range(len(vectors)+1):
	lobj = ax.plot([],[])[0]
	lines.append(lobj)

def init():
	for line in lines:
		line.set_data([],[])
	return lines

def ePow(r,a,x,t):
	return r*np.cos(x*t+a), r*np.sin(x*t+a)

def convertTuple(tup): 
    str =  ''.join(tup) 
    return str

def update(t):
	global lines
	vec = [0,0]
	for i, vector in enumerate(vectors):
		f = ePow(vector[0],vector[1],vector[2],t)
		lines[i].set_data([vec[0],f[0]+vec[0]],[vec[1],f[1]+vec[1]])
		vec[0] += f[0]
		vec[1] += f[1]
	xdata.append(vec[0])
	ydata.append(vec[1])

	'''
	sf = polygonFunction(t)
	xdata.append(sf[0])
	ydata.append(sf[1])
	'''

	lines[-1].set_data(xdata, ydata)

	return lines
	

ani = FuncAnimation(fig, update, frames=np.linspace(0, 1, 100),
                    init_func=init, blit=True)

plt.show()