######################## Description ############################
# A simple scripts which solves all the                         #
# 'find the differences' games! the scripts loads two images    #
# and marks in red the different pixels/area in the images.     #
# Syntax: imagediff <path-to-image1> <path-to-image2>           #
# Example: imagediff ./sample_image.jpg ./sample_image2.jpg     #
# Author: Ofek Bader                                            #
# Version: 1.0                                                  #
# Last Updated: 30/03/2019                                      #
# Python Version: 2.7.10                                        #
# Dependencies: Pillow v5.4.1 (a PIL fork)                      #
#################################################################
from PIL import Image
from sys import argv,exit

# Version 1
## imagediff fuctions colors in red the differences between two images.
## Input: two images as pixels list
## Output: a pixels list of the new image with different parts coloured in red.
def imagediff(pixels1, pixels2):
    epsilon = 20
    pixelsdiff = []
    for i in range(0,min(len(pixels1),len(pixels2))):
        pixeltemp = []
        for c in range(0,3):
            if abs(pixels1[i][c]-pixels2[i][c])<epsilon:
                pixeltemp.append(pixels1[i][c])
                continue
            else:
                pixeltemp = [255,15,15]
                break

        pixelsdiff.append((pixeltemp[0],pixeltemp[1],pixeltemp[2]))
    return pixelsdiff

# Version 2 - in order to get less false-positive, we use AVG value of all 3 colors of a pixels to determine
# a change.
## imagediff fuctions colors in red the differences between two images.
## Input: two images as pixels list
## Output: a pixels list of the new image with different parts coloured in red.
def imagediff2(pixels1, pixels2):
    epsilon = 15
    pixelsdiff = []
    for i in range(0,min(len(pixels1),len(pixels2))):
        pixeltemp = []
        sum1 = pixels1[i][0]+pixels1[i][1]+pixels1[i][2]
        sum2 = pixels2[i][0]+pixels2[i][1]+pixels2[i][2]
        avgdelta = abs((sum1)-(sum2))/3
        if avgdelta<epsilon:
            pixelsdiff.append(pixels1[i])
        else:
            pixelsdiff.append((255,15,15))


    return pixelsdiff

# Version 3 - in order to improve it and decrease the false-positive the function
# calculates the average of all 9 nearest pixels (a square).
## imagediff fuctions colors in red the differences between two images.
## Input: two images as pixels list
## Output: a pixels list of the new image with different parts coloured in red.
def imagediff3(pixels1, pixels2):
    epsilon = 15
    pixelsdiff = []
    for i in range(1,min(len(pixels1),len(pixels2))-1):
        pixeltemp = []
        sum1 = pixels1[i-1][0]+pixels1[i-1][1]+pixels1[i-1][2]+pixels1[i][0]+pixels1[i][1]+pixels1[i][2]+pixels1[i+1][0]+pixels1[i+1][1]+pixels1[i+1][2]   
        sum2 = pixels2[i-1][0]+pixels2[i-1][1]+pixels2[i-1][2]+pixels2[i][0]+pixels2[i][1]+pixels2[i][2]+pixels2[i+1][0]+pixels2[i+1][1]+pixels2[i+1][2]

        avgdelta = abs((sum1/9)-(sum2/9))
        if avgdelta<epsilon:
            pixelsdiff.append(pixels1[i])
        else:
            pixelsdiff.append((255,15,15))

    return pixelsdiff

#### Program ####
if len(argv) != 3:
    print('Syntax: imagediff <path-to-image1> <path-to-image2>')
    exit('Not enough arguments.')

#./samples/sample3/sample_image.jpg
#./samples/sample3/sample_image2.jpg
try:
    img     = Image.open(argv[1])
    img2    = Image.open(argv[2])
except:
    print('Error while loading images, please check the given filepath is correct.')
    exit('File not found')

pixels1 = list(img.getdata())
pixels2 = list(img2.getdata())


pixelsdiff = imagediff3(pixels1,pixels2)
imgdiff = Image.new(img.mode, img.size) # TODO:check ffor img.size might not be as img2.size
imgdiff.putdata(pixelsdiff)

imgdiff.show()