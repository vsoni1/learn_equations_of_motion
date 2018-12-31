import numpy as np
from PDE_FIND import *

def get_system(D0,xmin=30,xmax=70,ymin=30,ymax=70):
    
	D = np.array(D0).T
	D = D[xmin:xmax,ymin:ymax,:]
	n,m,steps = D.shape
	Wn = D.reshape(n,m,steps)
	xtemp = np.arange(5,n-5)
	ytemp = np.arange(5,n-5)
	ttemp = np.arange(5,steps,30)
	xx,yy,tt = np.meshgrid(xtemp,ytemp,ttemp)
	x = np.reshape(xx,np.prod(np.shape(xx)))
	y = np.reshape(yy,np.prod(np.shape(yy)))
	t = np.reshape(tt,np.prod(np.shape(tt)))
	points = [[x[i],y[i],t[i]] for i in range(len(x))]
	num_points = np.prod(np.shape(points))
	boundary = 5
	boundary_x = 5
	w = np.zeros((num_points,1))
	wt = np.zeros((num_points,1))
	wx = np.zeros((num_points,1))
	wy = np.zeros((num_points,1))
	wxx = np.zeros((num_points,1))
	wxy = np.zeros((num_points,1))
	wyy = np.zeros((num_points,1))
	N = 2*boundary-1  # odd number of points to use in fitting
	Nx = 2*boundary_x-1  # odd number of points to use in fitting
	deg = 5 # degree of polynomial to use

	for p in range(len(points)):
	    [x,y,t] = points[p]
	    w[p] = Wn[x,y,t]
	    wt[p] =  PolyDiffPoint(
            Wn[x,y,t-(N-1)/2:t+(N+1)/2], 
            np.arange(len(Wn[x,y,t-(N-1)/2:t+(N+1)/2])), 
            deg, 1
        )[0]
	    x_diff = PolyDiffPoint(
            Wn[x-(N-1)/2:x+(N+1)/2,y,t], 
            np.arange(len(Wn[x-(N-1)/2:x+(N+1)/2,y,t])), 
            deg, 2
        )
	    y_diff = PolyDiffPoint(
            Wn[x,y-(N-1)/2:y+(N+1)/2,t], 
            np.arange(len(Wn[x,y-(N-1)/2:y+(N+1)/2,t])), 
            deg, 2
        )
	    wx[p] = x_diff[0]
	    wy[p] = y_diff[0]
	    x_diff_yp = PolyDiffPoint(
            Wn[x-(Nx-1)/2:x+(Nx+1)/2,y+1,t],
            np.arange(len(Wn[x-(Nx-1)/2:x+(Nx+1)/2,y+1,t])),
            deg, 2
            )
	    x_diff_ym = PolyDiffPoint(
            Wn[x-(Nx-1)/2:x+(Nx+1)/2,y-1,t], 
            np.arange(len(Wn[x-(Nx-1)/2:x+(Nx+1)/2,y-1,t])), 
            deg, 2
        )
	    wxx[p] = x_diff[1]
	    wxy[p] = (x_diff_yp[0]-x_diff_ym[0])/(2)
	    wyy[p] = y_diff[1]
    
	X_data = np.hstack([w])
	X_ders = np.hstack([np.ones((num_points,1)), wx, wy, wxx, wxy, wyy])
	X_ders_descr = ['','w_{x}', 'w_{y}','w_{xx}','w_{xy}','w_{yy}']
	X, description = build_Theta(
        X_data, X_ders, X_ders_descr, 2, data_description = ['w']
        )
	
	return X, wt, description