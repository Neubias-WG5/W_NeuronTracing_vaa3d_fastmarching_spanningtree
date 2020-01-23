import os
import numpy as np
import imageio
#from PIL import Image

#Use a custom Bresenham 3D line algorithm
#Adapted from https://gist.github.com/yamamushi/5823518
def bresenham3DLine(x1, y1, z1, x2, y2, z2):
    point_list = []    
    
    point = []
    
    point.append(x1)
    point.append(y1)
    point.append(z1)
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    if dx < 0:
        x_inc =- 1
    else:
        x_inc = 1    
    l = abs(dx);

    if dy < 0:
        y_inc =- 1
    else:
        y_inc = 1    
    m = abs(dy)
    
    if dz < 0:
        z_inc =- 1
    else:
        z_inc = 1    
    n = abs(dz)
    
    dx2 = l * 2;
    dy2 = m * 2;
    dz2 = n * 2;
    
    if ((l >= m) and (l >= n)):
        err_1 = dy2 - l
        err_2 = dz2 - l
        for i in range(0, l):
            new_point=[point[0],point[1],point[2]]
            point_list.append(new_point)
            #print 'Point {},{},{}'.format(point[0], point[1], point[2])
            if (err_1 > 0):
                point[1] += y_inc
                err_1 -= dx2
            
            if (err_2 > 0):
                point[2] += z_inc
                err_2 -= dx2
            
            err_1 += dy2;
            err_2 += dz2;
            point[0] += x_inc
        
    elif ((m >= l) and (m >= n)):
        err_1 = dx2 - m
        err_2 = dz2 - m
        for i in range(0, m):       
            new_point = [point[0],point[1],point[2]]
            point_list.append(new_point)     
            #print 'Point {},{},{}'.format(point[0], point[1], point[2])
            if (err_1 > 0):
                point[0] += x_inc
                err_1 -= dy2
            
            if (err_2 > 0):
                point[2] += z_inc
                err_2 -= dy2
            
            err_1 += dx2
            err_2 += dz2
            point[1] += y_inc
        
    else:
        err_1 = dy2 - n
        err_2 = dx2 - n
        for i in range(0, n):    
            new_point = [point[0], point[1], point[2]]
            point_list.append(new_point)        
            #print 'Point {},{},{}'.format(point[0], point[1], point[2])
            if (err_1 > 0):
                point[1] += y_inc
                err_1 -= dz2
            
            if (err_2 > 0):
                point[0] += x_inc
                err_2 -= dz2
            
            err_1 += dy2
            err_2 += dx2
            point[2] += z_inc
        
    
    new_point = [point[0], point[1], point[2]]
    point_list.append(new_point)
    #print 'Point {},{},{}'.format(point[0], point[1], point[2])
    return point_list



def swc_to_tiff_stack(file_name, output_path, im_size,\
 align=False, offset=None, depth="Y", filter=range(10)):
    #dimensionArray=swcToTiffStack(file_name,align,offset,\depth,filter)    
    #Parse the SWC format
    #See http://www.neuronland.org/NLMorphologyConverter/MorphologyFormats/SWC/Spec.html
    
    #width =dimensionArray[0]
    #height=dimensionArray[1]
    #depth =dimensionArray[2]
    #min_x  =dimensionArray[3]
    #min_y  =dimensionArray[4]
    #min_z  =dimensionArray[5]
    print(file_name)
    
    x = open(file_name,'r')
    soma = None
    SWC = {}
    for line in x:
        if(not line.startswith('#') and not line == '\n'):
            #print line
            splits = line.split()
            #print splits
            index = int(splits[0])
            if index == 1:
                if offset == None:
                    soma_x = float(splits[2])
                    soma_y = float(splits[3])
                    soma_z = float(splits[4])
                else:
                    soma_x = float(splits[2]) + offset[0]
                    soma_y = float(splits[3]) + offset[1]
                    soma_z = float(splits[4]) + offset[2]

            n_type = int(splits[1])
            if not align:
                if offset == None:
                    x = float(splits[2])
                    y = float(splits[3])
                    z = float(splits[4])
                else:
                    x = float(splits[2]) + offset[0]
                    y = float(splits[3]) + offset[1]
                    z = float(splits[4]) + offset[2]           
            else:
                x = float(splits[2]) - soma_x
                y = float(splits[3]) - soma_y
                z = float(splits[4]) - soma_z         
            r = float(splits[5])
            parent = int(splits[-1])
            #if n_type in filter:
            SWC[index] = (int(x), int(y), int(z), r, parent, n_type)
    #Now identify the bigger small and larger x/y and z
    
    max_x = 0
    max_y = 0
    max_z = 0
    min_x = 0
    min_y = 0
    min_z = 0
#    min_x=1000000
#    min_y=1000000
#    min_z=1000000
#    for index in SWC.keys():
#        C = SWC[index]
#        max_x = C[0] if C[0] > max_x else max_x
#        max_y = C[1] if C[1] > max_y else max_y
#        max_z = C[2] if C[2] > max_z else max_z
#        
#        min_x = C[0] if C[0] < min_x else min_x
#        min_y = C[1] if C[1] < min_y else min_y
#        min_z = C[2] if C[2] < min_z else min_z
    
#    print 'max_x:{} max_y:{} max_z:{}'.format(max_x,max_y,max_z)
#    print 'min_x:{} min_y:{} min_z:{}'.format(min_x,min_y,min_z)
    
#    width=int(max_x-min_x+1)
#    height=int(max_y-min_y+1)
#    depth=int(max_z-min_z+1)
    width = im_size[0]
    height = im_size[1]
    depth = im_size[2]
    
    print('Image width:{} height:{} depth:{}'.format(width, height, depth))
    
    #Create a 3D images of this size
    #Row,Column,Depth == height x width x depth
    image_array = np.zeros([height, width, depth], dtype = np.uint8)
    #Define the list of row (y) rr, column (x) cc and depth (z) dd
    #All the pixel coordinate will be stored them in order to easily populate the matrix image_array
    rr = []
    cc = []
    dd = []
    
    #Now, loops through all index and create the line between different points in 3D
    for index in SWC.keys():
        #print index
        if index < 2:
            continue
        C = SWC[index]
        parentPointIndex=C[4]
        #
        if parentPointIndex==-1:
            continue
        #print C
        #print SWC
        P = SWC[parentPointIndex] # C[4] is parent index
    
        #compute the Bresenham 3d Line between 2 point
        #substract with the min(x/y/z) to avoid negative coordinate so it will be easier to fill up the numpy matrix        
        result = bresenham3DLine(int(P[0]-min_x), int(P[1]-min_y), int(P[2]-min_z), int(C[0]-min_x), int(C[1]-min_y), int(C[2]-min_z))
        #result=bresenhamline(s, np.zeros(s.shape[1]), max_iter=-1)
        min_point_x = min(P[0]-min_x, C[0]-min_x)
        max_point_x = max(P[0]-min_x, C[0]-min_x)
        min_point_y = min(P[1]-min_y, C[1]-min_y)        
        max_point_y = max(P[1]-min_y, C[1]-min_y)
        min_point_z = min(P[2]-min_z, C[2]-min_z)
        max_point_z = max(P[2]-min_z, C[2]-min_z)
        
        #print('Point 1 {},{},{}'.format(P[0], P[1], P[2]))
        #print('Point 2 {},{},{}'.format(C[0], C[1], C[2]))
        #print('min_point_x:{} max_point_x:{} min_point_y:{} max_point_y:{} min_point_z:{} max_point_z:{}').format(min_point_x,max_point_x,min_point_y,max_point_y,min_point_z,max_point_z)
        
        #Check which x/y/z is the smaller and which one is the bigger
        #print result
        #Loop though all the point and set the value to 1 in the image_array
        #Declare the row/col/depth array used to fill
        for point in result:
            #print point
            #Make sure the line point are constraints into the segment boundary
            #May be unnecessary, depend of the implementation of the bresenhamline algorithm
            if(max_point_x >= point[0] and point[0] >= min_point_x and max_point_y >= point[1] \
                and point[1] >= min_point_y and max_point_z >= point[2] and point[2] >= min_point_z):
                rr.append(point[1])
                cc.append(point[0])
                dd.append(point[2])
    
    #Populate the 3D Matrix Image
    arrayDimension = image_array.shape
    #Get Z dimension to loop over it
    #zDimension = arrayDimension[2]
    #Fill the matrix with the line pixels for a value of 255
    image_array[rr, cc, dd] = 255 #1   
    image_array = np.moveaxis(image_array,2,0)
    imageio.volwrite(os.path.join(output_path, file_name[:-4] + '.tif'), image_array)
    #imwrite(output_path+'result_vaa3d.tif', image_array, is_2d=False
 
    #for z in range(0,zDimension):
    #    image1 = image_array[:, :,z]
    #    #print 'Image 1'
    #    print('Save Z {}'.format(z))
    #    Image.fromarray(image1, mode='L').save(output_path+'image{:03}.tif'.format(z))
    #return(image_array)
