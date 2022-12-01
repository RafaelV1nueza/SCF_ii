# -*- coding: utf-8 -*-
"""
@author: Rafael Vinueza
"""
#x = w-
#y = y
#z = z
#w = x

import numpy as np
#import random


def quaternion_multiply(quaternion1, quaternion0):
    x0, y0, z0, w0 = quaternion0
    x1, y1, z1, w1 = quaternion1
    return np.array([x1 * w0 + y1 * z0 - z1 * y0 + w1 * x0,
                     -x1 * z0 + y1 * w0 + z1 * x0 + w1 * y0,
                     x1 * y0 - y1 * x0 + z1 * w0 + w1 * z0,
                     -x1 * x0 - y1 * y0 - z1 * z0 + w1 * w0], dtype=np.float64)
def conjugate(quat):
    # invert x,y,z and leave w as is
    return np.array(
        [
            -quat[0],
            -quat[1],
            -quat[2],
            quat[3]
        ],
        dtype=quat.dtype
    )
def multy_multiply(*quats):
    qf = np.array([0,0,0,1])
    print("   {0}".format(qf))
    for quat in quats:
        qf = quaternion_multiply(qf, quat)
        print(" x {0}".format(quat))
    print("= \n{0}\n".format(qf))
    return qf
def axis_tf(axis,quaternion):
    #Quaternion rules
    #i^2=j^2=k^2=ijk=-1
    #ij = k
    #ji = -k
    
    inv_q = conjugate(quaternion)
    ax,ay,az,aw = quaternion #i,j,k,w
    cx,cy,cz,one_axis = axis #i,j,k
    bx,by,bz,bw = inv_q #i,j,k,w
    #ax*cx(-w)+ax*cy(k)+ax*cz(-j)+ay*cx(-k)+ay*cy(-w)+ay*cz(i)
    # +az*cx(j)+az*cy(-i)+az*cz(-w)+aw*cx(i)+aw*cy(j)+aw*cz(k)
    
    vw = -ax*cx-ay*cy-az*cz+aw#w?
    
    vx = ay*cz-az*cy+aw*cx+ax#i
    vy = -ax*cz+az*cx+aw*cy+ay#j
    vz = ax*cy-ay*cx+aw*cz+az#k
    #print(np.array([float(vx),float(vy),float(vz),float(vw)]))
    
    #vw*bx(i)+vw*by(j)+vw*bz(k)+vw*bw(w)+vx*bx(-w)+vx*by(k)+vx*bz(-j)+vx*bw(i)
    #  +vy*bx(-k)+vy*by(-w)+vy*bz(i)+vy*bw(j)+vz*bx(j)+vz*by(-i)+vz*bz(-w)+vz*bw(k)
    
    dw = vw*bw-vx*bx-vy*by-vz*bz
    dx = vw*bx+vx*bw+vy*bz-vz*by
    dy = vw*by-vx*bz+vy*bw+vz*bx
    dz = vw*bz+vx*by-vy*bx+vz*bw
    
    vect = np.array([round(dx,6),round(dy,6),round(dz,6),round(dw,6)])
    return vect
    
    
if  __name__ == "__main__":
    #Define the axis
    x_axis = np.array([1, 0, 0, 1])
    y_axis = np.array([0, 1, 0, 1])
    z_axis = np.array([0, 0, 1, 1])  
    #Movementrs
    xp30 = np.array([ 0.258819, 0, 0, 0.9659258 ])#+30grados en x
    xp45 = np.array([ 0.3826834, 0, 0, 0.9238795 ])#+45 grados en x
    xn45 = np.array([ -0.3826834, 0, 0, 0.9238795 ])#+45 grados en x
    yp45 = np.array([ 0, 0.3826834, 0, 0.9238795 ])#+45 grados en y
    yn45 = np.array([ 0, -0.3826834, 0, 0.9238795 ])#+45 grados en y
    zn45 = np.array([ 0, 0, 0.3826834, 0.9238795 ])#+45 grados en z
    zn45 = np.array([ 0, 0, -0.3826834,0.9238795 ])#+45 grados en z
    xp90 = np.array([ 0.7071068, 0, 0, 0.7071068 ]) #+90 grados en x
    xn90 = np.array([ -0.7071068, 0, 0, 0.7071068 ]) #-90 grados en x
    yp90 = np.array([ 0, 0.7071068, 0, 0.7071068 ]) #+90 grados en y
    yn90 = np.array([ 0, -0.7071068, 0, 0.7071068 ]) #-90 grados en y
    zp90 = np.array([ 0, 0, 0.7071068, 0.7071068 ]) #+90 grados en z
    zn90 = np.array([ 0, 0, -0.7071068, 0.7071068 ]) #-90 grados en z
    xp180 = np.array([ 1, 0, 0, 0 ]) #+180 grados en x
    xn180 = np.array([ -1, 0, 0, 0 ]) #-180 grados en x
    yp180 = np.array([ 0, 1, 0, 0 ]) #+180 grados en y
    yn180 = np.array([ 0, -1, 0, 0 ]) #-180 grados en y
    zp180 = np.array([ 0, 0, 1, 0 ]) #+180 grados en z
    zn180 = np.array([ 0, 0, -1, 0 ]) #-180 grados en z
    unit = np.array([ 0, 0, 0, 1 ]) #-180 grados en z
    print("Original Axis:")
    print("   {0}\n   {1}\n   {2}\n".format(x_axis,y_axis,z_axis))
    #multiply
    print("Quaternion Transformation: ")
    #Transform your quaternions here
    # Everyone gets a quaternion
    #----------------------------------------------------------------
    finalq = multy_multiply(xp30,zp90)
    #----------------------------------------------------------------
    x_axis = axis_tf(x_axis, finalq)
    y_axis = axis_tf(y_axis, finalq)
    z_axis = axis_tf(z_axis, finalq)
    t = np.array([x_axis,y_axis,z_axis])

    print("Modified Axis:")
    #print("   X axis: {0}\n   Y axis: {1}\n   Z axis: {2}\n".format(x_axis,y_axis,z_axis))
    print(t)
    
    

    
    


