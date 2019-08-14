# FourierPlotter
Draw any arbitrary continuous curve using an infinite sum of rotating vectors each at different lengths and rotating at different frequencies.

The work here was inspired by the video https://www.youtube.com/watch?v=r6sGWTCMz2k which goes into detail about the more generalized form of using
fourier series to draw any continous boundary using a sum of rotating vectors in the complex plane.

The python code in this repository can be used to animate the drawing of defined boundaries by calculating the series of rotating vectors required to do so. 
The math for how this works is explained in the video above, each vector has its own length, starting position, and rotation frequency. The more vectors
that are used the more accurate the created boundary is to the actual defined boundary curve. 

The remarkable thing is that by having a self contained function of time with a set number of weights we can draw any arbitary continous curve that we
desire. For example check out drawing a square or triangle below.

![](https://github.com/awbrown90/FourierPlotter/blob/master/fourier_triangle.gif)

![](https://github.com/awbrown90/FourierPlotter/blob/master/fourier_square.gif)

