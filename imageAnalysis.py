###################################################
# APS106 - Winter 2023 - Lab 8 - Corner Detection #
###################################################

# Uncomment the line below to use the image utility functions to load and display your images
#from lab8_image_utils import display_image, image_to_pixels
from operator import itemgetter

################################################
# PART 1 - RGB to Grayscale Conversion         #
################################################

def rgb_to_grayscale(rgb_img):
    """
    (tuple) -> tuple
    
    Function converts an image of RGB pixels to grayscale.
    Input tuple is a nested tuple of RGB pixels.
    
    The intensity of a grayscale pixel is computed from the intensities of
    RGB pixels using the following equation
    
        grayscale intensity = 0.3 * R + 0.59 * G + 0.11 * B
    
    where R, G, and B are the intensities of the R, G, and B components of the
    RGB pixel. The grayscale intensity should be *rounded* to the nearest
    integer.
    """
    
    ## TODO complete the function
    grey_img=()
    for tup in rgb_img:
        grey_img+=round(0.3*tup[0]+0.59*tup[1]+0.11*tup[2]),
    return grey_img
            
            
############################
# Part 2b - Dot Product    #
############################

def dot(x,y):
    """
    (tuple, tuple) -> float
    
    Performs a 1-dimensional dot product operation on the input vectors x
    and y. 
    """
    
    ## TODO complete the function
    prod=0
    if len(x)==len(y):
        for i in range(len(x)):
            prod+=float(x[i]*y[i])
    else:
        return False
    return prod


######################################
# Part 2c - Extract Image Segment    #
######################################

def extract_image_segment(img, width, height, centre_coordinate, N):
    """
    (tuple, int, int, tuple, int) -> tuple
    
    Extracts a 2-dimensional NxN segment of a image centred around
    a given coordinate. The segment is returned as a tuple of pixels from the
    image.
    
    img is a tuple of grayscale pixel values
    width is the width of the image
    height is the height of the image
    centre_coordinate is a two-element tuple defining a pixel coordinate
    N is the height and width of the segment to extract from the image
    
    """
    ## TODO complete the function
    
    if N > width or N>height:
        return 0

    i=0
    matTup = tuple()
    rowTup = tuple()
    while i<len(img):
        rowTup = tuple()
        for j in range(i, width+i):
            rowTup += img[i],
            i+=1
        matTup+=rowTup,
    
    
    start = int((N-1)/2)
    restup=tuple()
    for i in range(centre_coordinate[1]-start, centre_coordinate[1]+start+1):
        for j in range(centre_coordinate[0]-start, centre_coordinate[0]+start+1):
            restup+=matTup[i][j],
        
    return restup
                      
######################################
# Part 2d - Kernel Filtering         #
######################################

def kernel_filter(img, width, height, kernel):
    """
    (tuple, int, int, tuple) -> tuple
    
    Apply the kernel filter defined within the two-dimensional tuple kernel to 
    image defined by the pixels in img and its width and height.
    
    img is a 1 dimensional tuple of grayscale pixels
    width is the width of the image
    height is the height of the image
    kernel is a 2 dimensional tuple defining a NxN filter kernel, n must be an odd integer
    
    The function returns the tuple of pixels from the filtered image
    """

    ## TODO complete the function
    N = len(kernel)
    tupleKer = tuple()
    for i in kernel:
        for j in i:
            tupleKer+=j,
    
    start=int((N-1)/2)
    elem=0
    mat=tuple()
    finalimg=tuple()
    
    for i in range(width):
        for j in range(height):
            elem=0
            if i==0 or j==0 or i>=width-start or j>=height-start:
                elem=0
            else:
                mat = extract_image_segment(img,width,height,(j,i),N)
                for xmat in range(len(tupleKer)):
                    elem=elem+mat[xmat]*tupleKer[xmat]
            finalimg+=round(elem),
    return finalimg

###############################
# PART 3 - Harris Corners     #
###############################

def harris_corner_strength(Ix,Iy):
    """
    (tuple, tuple) -> float
    
    Computes the Harris response of a pixel using
    the 3x3 windows of x and y gradients contained 
    within Ix and Iy respectively.
    
    Ix and Iy are  lists each containing 9 integer elements each.

    """

    # calculate the gradients
    Ixx = [0] * 9
    Iyy = [0] * 9
    Ixy = [0] * 9
    
    for i in range(len(Ix)):
        Ixx[i] = (Ix[i] / (4*255))**2
        Iyy[i] = (Iy[i] / (4*255))**2
        Ixy[i] = (Ix[i] / (4*255) * Iy[i] / (4*255))
    
    # sum  the gradients
    Sxx = sum(Ixx)
    Syy = sum(Iyy)
    Sxy = sum(Ixy)
    
    # calculate the determinant and trace
    det = Sxx * Syy - Sxy**2
    trace = Sxx + Syy
    
    # calculate the corner strength
    k = 0.03
    r = det - k * trace**2
    
    return r

def harris_corners(img, width, height, threshold):
    """
    (tuple, int, int, float) -> tuple
    
    Computes the corner strength of each pixel within an image
    and returns a tuple of potential corner locations. Each element in the
    returned tuple is a two-element tuple containing an x- and y-coordinate.
    The coordinates in the tuple are sorted from highest to lowest corner
    strength.
    """
    
    # perform vertical edge detection
    vertical_edge_kernel = ((-1, 0, 1),
                            (-2, 0, 2),
                            (-1, 0, 1))
    Ix = kernel_filter(img, width, height, vertical_edge_kernel)
    
    # perform horizontal edge detection
    horizontal_edge_kernel = ((-1,-2,-1),
                              ( 0, 0, 0),
                              ( 1, 2, 1))
    Iy = kernel_filter(img, width, height, horizontal_edge_kernel)
    
    # compute corner scores and identify potential corners
    border_sz = 1
    corners = []
    for i_y in range(border_sz, height-border_sz):
        for i_x in range(border_sz, width-border_sz):
            Ix_window = extract_image_segment(Ix, width, height, (i_x, i_y), 3)
            Iy_window = extract_image_segment(Iy, width, height, (i_x, i_y), 3)
            corner_strength = harris_corner_strength(Ix_window, Iy_window)
            if corner_strength > threshold:
                #print(corner_strength)
                corners.append([corner_strength,(i_x,i_y)])

    # sort
    corners.sort(key=itemgetter(0),reverse=True)
    corner_locations = []
    for i in range(len(corners)):
        corner_locations.append(corners[i][1])

    return tuple(corner_locations)


###################################
# PART 4 - Non-maxima Suppression #
###################################

def non_maxima_suppression(corners, min_distance):
    """
    (tuple, float) -> tuple
    
    Filters any corners that are within a region with a stronger corner.
    Returns a tuple of corner coordinates that are at least min_distance away from
    any other stronger corner.
    
    corners is a tuple of two-element coordinate tuples representing potential
        corners as identified by the Harris Corners Algorithm. The corners
        are sorted from strongest to weakest.
    
    min_distance is a float specifying the minimum distance between any
        two corners returned by this function
    """
    
    ## TODO complete the function
    new_corners=tuple()
    new_corners+=corners[0],
    dist=0
    for corn in corners:
        check_all = True
        for res in new_corners:
            dist=((corn[0]-res[0])**2 + (corn[1]-res[1])**2)**(1/2)
            if(dist<min_distance):
                check_all = False
        if(check_all):
           new_corners+= corn,
           
    return new_corners