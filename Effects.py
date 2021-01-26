from math import sqrt
from cv2 import addWeighted,  GaussianBlur, split, merge, getRotationMatrix2D, warpAffine
from PIL import Image

import numpy as np

"""
This Module has functions that are capable of modify images and returns image array 
Round Corner - Add Round corners to the image 
AddColour2Pixel - Add colour to each colour pixel
BlendColour - Blend the colour to image based on the blend alpha
Blur - Blur the image by Distort value
BlendImage - Blend two images together based on the blend alpha 
Rotate - Rotate the image by angle
Shadow - Create shadow to the image based on offset and shadow colour
Elevate - Elevate image based on elevation
RGB2RGBA - Change image from 3 channel to 4 channel 
"""


def RoundCorner(ImageArray, Radius_LT, Radius_RT, Radius_RB, Radius_LB):
    """
    Param:
        ImageArray: should be a numpy array
        Radius(_LT,_LB,_RB,_RT): can be float or int
    This method will return a image list which is to be converted to numpy array then to image
    Image Array can be either be three channel or four channel (RGB or RGBA)
    Return:
         Returns a Image array
         Image array will be four channel
    """
    RC_Image = []
    Height = len(ImageArray)
    Width = len(ImageArray[0])
    Y_LT = 0
    Y_RT = Width
    Y_LB = 0
    Y_RB = Width
    for row in range(Height):
        RC_Row = []
        if row <= Radius_RT:
            Y_RT = sqrt(Radius_RT * Radius_RT - (row - Radius_RT) * (row - Radius_RT)) - Radius_RT + Width
            if Y_RT < 0:
                Y_RT = -Y_RT
        if row <= Radius_LT:
            Y_LT = sqrt(Radius_LT * Radius_LT - (row - Radius_LT) * (row - Radius_LT)) - Radius_LT
            if Y_LT < 0:
                Y_LT = -Y_LT
        if row >= Height - Radius_LB:
            x = Height - Radius_LB
            Y_LB = sqrt(Radius_LB * Radius_LB - (row - x) * (row - x)) - Radius_LB
            if Y_LB < 0:
                Y_LB = -Y_LB
        if row >= Height - Radius_RB:
            x = Height - Radius_RB
            Y_RB = sqrt(Radius_RB * Radius_RB - (row - x) * (row - x)) - Radius_RB + Width
            if Y_RB < 0:
                Y_RB = -Y_RB
        for column in range(len(ImageArray[row])):
            RC_Column = []
            # Setting RGBA Component
            if len(ImageArray[row][column]) == 3:
                R, G, B = ImageArray[row][column]
                A = 255
            else:
                R, G, B, A = ImageArray[row][column]

            if column < Y_LT:
                RC_Column.append(R)
                RC_Column.append(G)
                RC_Column.append(B)
                RC_Column.append(0)
            elif column > Y_RT:
                RC_Column.append(R)
                RC_Column.append(G)
                RC_Column.append(B)
                RC_Column.append(0)
            elif column < Y_LB:
                RC_Column.append(R)
                RC_Column.append(G)
                RC_Column.append(B)
                RC_Column.append(0)
            elif column > Y_RB:
                RC_Column.append(R)
                RC_Column.append(G)
                RC_Column.append(B)
                RC_Column.append(0)
            else:
                RC_Column.append(R)
                RC_Column.append(G)
                RC_Column.append(B)
                RC_Column.append(A)
            RC_Column = np.asarray(RC_Column)
            RC_Row.append(RC_Column)
        RC_Image.append(RC_Row)
    return RC_Image


def AddColour2Pixel(ImageArray, Colour):
    """
    Param:
        ImageArray: should be a numpy array
        Colour : should be 4 channel array
    This method will return a image list which is to be converted to numpy array then to image
    Image Array can be either be three channel or four channel (RGB or RGBA)
    Return:
         Returns a Image array
         Image array will be four channel
    """
    Height = len(ImageArray)
    Width = len(ImageArray[0])
    Channel = len(ImageArray[0][0])

    ColouredImage = []
    if Channel == 4:
        ImageArray = RGB2RGBA(ImageArray)
    for i in range(Height):
        for j in range(Width):
            Temp = []
            for k in range(Channel):
                val = ImageArray[i][j][k] + Colour[k]
                if val > 255:
                    Temp.append(255)
                else:
                    Temp.append(val)
            ColouredImage.append(Temp)

    return np.array(ColouredImage).reshape((Height, Width, Channel))


def BlendColour(ImageArray, Colour, BlendAlpha=0.5):
    """
    Param:
        ImageArray: should be a numpy array
        Colour: it should be 4 channel array
        BlendAlpha: sets the intensity of the blend
    This method will return a image list which is to be converted to numpy array then to image
    Image Array can be either be three channel or four channel (RGB or RGBA)
    Return:
         Returns a Image array
         Image array will be four channel
    """
    Height = len(ImageArray)
    Width = len(ImageArray[0])
    Channel = len(ImageArray[0][0])
    if Channel == 4:
        ImageArray = RGB2RGBA(ImageArray)

    BlendColouredImage = []
    for i in range(Height):
        for j in range(Width):
            Temp = []
            for k in range(Channel):
                val = int(ImageArray[i][j][k] * (1 - BlendAlpha) + Colour[k] * BlendAlpha)
                if val > 255:
                    Temp.append(255)
                else:
                    Temp.append(val)
            BlendColouredImage.append(Temp)

    return np.array(BlendColouredImage).reshape((Height, Width, Channel))


def Blur(ImageArray, Distort):
    """
    Param:
        ImageArray: Get an Image array or list
        Distort: This set the distortion amount in image
    Return:
        Returns a blurred image array
    """
    return GaussianBlur(ImageArray, (Distort, Distort), 0)


def BlendImage(ImageArray, ImageArray1, BlendAlpha=0.5):
    """
    Param:
        ImageArray: should be a numpy array
        ImageArray1: should be a numpy array
        BlendAlpha: sets the intensity of the blend
    This method will return a image list which is to be converted to numpy array then to image
    Image Array can be either be three channel or four channel (RGB or RGBA)
    Return:
         Returns a Image array
         Image array will be four channel
    """
    return addWeighted(ImageArray, (1 - BlendAlpha), ImageArray1, BlendAlpha, 0)


def Rotate(ImageArray, Angle):
    """
        Param:
            ImageArray: should be a numpy array
            Rotate: angle to be rotated
        This method will return a image list which is to be converted to numpy array then to image
        Image Array can be either be three channel or four channel (RGB or RGBA)
        Return:
             Returns a Image array
             Image array will be four channel
        """
    H = len(ImageArray)
    W = len(ImageArray[0])

    cX = W / 2
    cY = H / 2

    M = getRotationMatrix2D((cX, cY), -Angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    nW = int((H * sin) + (W * cos))
    nH = int((H * cos) + (W * sin))

    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    return warpAffine(ImageArray, M, (nW, nH), borderValue=(0, 0, 0, 0))


def Shadow(ImageArray, Offset, ShadowColour):
    """
        Param:
            ImageArray: should be a numpy array
            Offset: position to be moved
            ShadowColour: Colour of the shadow
        This method will return a image list which is to be converted to numpy array then to image
        Image Array can be either be three channel or four channel (RGB or RGBA)
        Return:
             Returns a Image array
             Image array will be four channel
        """
    Height = len(ImageArray)
    Width = len(ImageArray[0])
    Channel = len(ImageArray[0][0])
    if Channel == 3:
        ImageArray = RGB2RGBA(ImageArray)

    ShadowImage = Image.new("RGBA", (Height + Offset[1] * 2, Width + Offset[0] * 2))

    ShadowImage.paste(ShadowColour, [Offset[0], Offset[1], Offset[0] + Width, Offset[1] + Height])
    Array = np.asarray(ShadowImage, np.uint8)
    Array = Blur(Array, 33)
    ShadowImage = Image.fromarray(Array)

    image = Image.fromarray(ImageArray)
    ShadowImage.paste(image, (0, 0))
    ShadowImage = np.asarray(ShadowImage, np.uint8)
    return ShadowImage


def Elevate(ImageArray, Elevation):
    """
        Param:
            ImageArray: should be a numpy array
            Elevation: Elevate distance
        This method will return a image list which is to be converted to numpy array then to image
        Image Array can be either be three channel or four channel (RGB or RGBA)
        Return:
             Returns a Image array
             Image array will be four channel
        """
    Elevation = Elevation + 10
    Height = len(ImageArray)
    Width = len(ImageArray[0])
    Channel = len(ImageArray[0][0])

    if Channel == 3:
        ImageArray = RGB2RGBA(ImageArray)

    ShadowImage = Image.new("RGBA", (Height + Elevation * 2, Width + Elevation * 2))

    ShadowImage.paste((20, 20, 20), [10, 10, 2 * Elevation - 10 + Width, 2 * Elevation - 10 + Height])
    Array = np.asarray(ShadowImage, np.uint8)
    Array = Blur(Array, 33)

    ShadowImage = Image.fromarray(Array)
    ShadowImage.paste(Image.fromarray(ImageArray), (Elevation, Elevation))
    ShadowImage = np.asarray(ShadowImage, np.uint8)

    return ShadowImage


def RGB2RGBA(ImageArray):
    """
        Param:
            ImageArray: should be a numpy array
        This method will return a image list which is to be converted to numpy array then to image
        Image Array can be either be three channel (RGB)
        Return:
             Returns a Image array
             Image array will be four channel
        """
    Channel = len(ImageArray[0][0])
    if Channel == 3:
        R, G, B = split(ImageArray)
        A = np.ones(B.shape, dtype=B.dtype) * 255
        return merge((R, G, B, A))
    return None
