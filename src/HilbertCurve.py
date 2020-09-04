import numpy as np

def HilbertValue(n, x, y):
    '''Function that return the index of point (x, y) after transformed to a Hilbert Curved of a grid nxn'''
    s = n//2
    qx, qy, d = 0, 0, 0
    while s > 0:
        qx = x //s #the x quadrant
        qy = y//s #the y quadrant
        d += abs(3*qx - qy)*s**2
        x, y = HilRotate(s, x, y, qx, qy) #rotate x and y
        s = s//2
    return d

def HilRotate(s, x, y, qx, qy):
    '''Function that realize the rotation from Hilbert Curve'''
    if qy == 0 and qx == 0: 
        #swap x and y
        t = x
        x = y
        y = t
        
    if qx == 1:
        x = x - s
        if qy == 0:
            t = x
            x = y
            y = t
            
            x = s - x - 1
            y = s - y - 1
    
    if qy == 1:
        y = y - s
        
        
    return x, y       
            
def MotionRugs(data, n, attr):
    '''
    Function that create a motion rugs image from a dataframe of frames
    
    Inputs:
        data - numpy array of dim [nº frames, nº entitys, nº variables]
        n - int, size of the grid to the HilbertCurve
        attr - variable to use on the image
        
    Output:
        img - numpy array of dim [nº entitys, nº frames]
    '''
    frames, ent, var = data.shape
    #move x and y to grid of size nxn
    data[:, :, 0] = np.floor((n- 1)*data[:, :, 0]/2000)
    data[:, :, 1] = np.floor((n- 1)*data[:, :, 1]/2000)
    #result img
    img = np.zeros((ent, frames))
    #iterate for each frame
    for i in range(frames):
        #new empty column
        new_line = np.zeros(ent)
        attr_line = data[i, :, attr]
        #for each entity
        for j in range(ent):
            new_line[j] = HilbertValue(n, data[i, j, 0], data[i, j, 1])
        new_line_inds = new_line.argsort()
        img[:, i] = attr_line[new_line_inds]
    return img

def convert_gray_scale(img):
    '''Function that convert image in any range, to range 0 to 255'''
    return img * 255 / img.max()
    
    
    
##########################
##########################
##BITWISE FROM WIKIPEDIA
##########################

def HilbertValueBit(n, x, y):
    '''Function that return the index of point (x,y) after transformed to a Hilbert Curve of a grid nxn'''
    s = n//2
    rx, ry, d = 0, 0, 0
    #Iterating until Hilbert Curve of 0 order
    while(s > 0):
        rx = (x & s) > 0 #if x > 0 and s > 0, rx = True, else false
        ry = (y & s) > 0 #if y > 0 and s > 0, rx = True, else false
        d += s*s*((3*rx)^ry)
        x, y = rot(n, x, y, rx, ry)
        s = s//2
    return d

def rot(n, x, y, rx, ry):
    if(ry == 0):
        if(rx == 1):
            x = n - 1 - x
            y = n - 1 - y
        t = x
        x = y
        y = t
    return x, y



