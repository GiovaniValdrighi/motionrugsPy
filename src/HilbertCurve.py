import numpy as np

def HilbertValue(n, x, y):
    '''
    Function that return the index of point (x, y) after transformed to a Hilbert Curved of a grid nxn
     
    Inputs:
        n (int) : size of the grid to fill with Hilbert Curve
        x (int) : first coordinate of point in grid
        y (int) : second coordinate of point in grid
    
    Output: 
        d (int) : Hilbert Curve index
    '''
    s = n//2 
    qx, qy, d = 0, 0, 0
    while s > 0:
        qx = x//s #the x quadrant
        qy = y//s #the y quadrant
        d += abs(3*qx - qy)*s*s
        x, y = HilRotate(s, x, y, qx, qy) #rotate x and y
        s = s//2
    return d

def HilRotate(s, x, y, qx, qy):
    '''
    Function that realize the rotation from Hilbert Curve
    
    If the point is out of the quadrant (0, 0), we first translate the point
    to be in it quadrant.
    '''
    x = x - s*qx
    y = y - s*qy
    
    if qy == 0:
        t = x
        x = y
        y = t
        if qx == 1:
            x = s - x - 1
            y = s - y - 1
    return x, y       
            
def MotionRugs(data, n, attr, xMax, yMax):
    '''
    Function that create a motion rugs image from a dataframe of frames
    
    Inputs:
        data - numpy array of dim [nº frames, nº entitys, nº variables]
        n - int, size of the grid to the HilbertCurve
        attr - variable to use on the image
        xMax - max value for variable x
        yMax - max value for variable y
        
    Output:
        img - numpy array of dim [nº entitys, nº frames]
    '''
    frames, ent, var = data.shape
    #move x and y to grid of size nxn
    data[:, :, 0] = np.floor((n- 1)*data[:, :, 0]/xMax)
    data[:, :, 1] = np.floor((n- 1)*data[:, :, 1]/yMax)
    #result img
    img = np.zeros((ent, frames))
    #iterate for each frame
    for i in range(frames):
        #new empty column
        new_line = np.zeros(ent)
        #for each entity
        for j in range(ent):
            new_line[j] = HilbertValue(n, data[i, j, 0], data[i, j, 1])
        new_line_inds = new_line.argsort()
        img[:, i] = data[i, :, attr][new_line_inds]
    return img

def convert_gray_scale(img):
    '''Function that convert image in any range, to range 0 to 255'''
    return img * 255 / img.max()

def colorMap(img, attrMax = None, attrMin = None):
    '''Function that create the color mapping from the image of attributes'''
    if not attrMax:
        attrMax = img.max()
    if not attrMin:
        attrMin = img.min()
    attrRange = attrMax - attrMin + 1
    
    colors = {0 : (165, 0, 38), 1 : (215, 48, 39),
              2 : (244, 109, 67), 3 : (253, 174, 97),
              4 : (254, 224, 144), 5: (224, 243, 248),
              6 : (171, 217, 233), 7 : (116, 173, 209),
              8 : (69, 117, 180) , 9: (49, 54, 149)}
    
    img_colors = np.zeros((img.shape[0], img.shape[1], 3))
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img_colors[i, j, :] = colors[np.floor(10*(img[i, j] - attrMin)/attrRange)]
    return img_colors