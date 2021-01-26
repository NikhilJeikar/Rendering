from Effects import Rotate,RGB2RGBA
from cv2 import circle
from math import sqrt

"""
This module returns set of images by adding effects
RotateAnimation: Returns a set of image by rotation based on frames per sec 
FocusOut: Create a circle from centre and moves out
FocusIn: Create circle from out and moves inside
"""


def RotateAnimation(ImageArray, Start, Stop,Time,Frames:int):
    """
    Param:
        ImageArray: should be a numpy array
        Start: start angle
        Stop: stop angle
        Time: Number of seconds the frames to be rendered
        Frames: Number of frames per second
    Image Array can be either be three channel or four channel (RGB or RGBA)
    Return:
         Returns a Stack of Image array
         Image array will be four channel
    """
    Channel = len(ImageArray[0][0])
    if Channel == 3:
        ImageArray = RGB2RGBA(ImageArray)
    Anim = {}
    Diff = (Stop - Start)/(Time*Frames)
    for i in range(Time*Frames):
        Image = Rotate(ImageArray, Start + (Diff*i))
        Anim[i] = Image
    return Anim


def FocusOut(ImageArray, Time: int, Frames: int):
    """
    Param:
        ImageArray: should be a numpy array
        Time: Number of seconds the frames to be rendered
        Frames: Number of frames per second
    Image Array can be either be three channel or four channel (RGB or RGBA)
    Return:
         Returns a Stack of Image array
         Image array will be four channel
    """
    Height = len(ImageArray)
    Width = len(ImageArray[0])
    Channel = len(ImageArray[0][0])
    Stack = []
    MaxRadius = sqrt((Height * Height) / 4 + (Width * Width) / 4)
    CenterCoordinates = (int(Width / 2), int(Height / 2))
    Color = (0, 0, 0, 0)
    Thickness = -1
    if Channel == 3:
        ImageArray = RGB2RGBA(ImageArray)
    for i in range(Time * Frames):
        Rad = int((MaxRadius / (Time * Frames)) * (i + 1))
        image = circle(ImageArray, CenterCoordinates, Rad, Color, Thickness)

        Stack.append(image)

    return Stack


def FocusIn(ImageArray, Time: int, Frames: int):
    """
    Param:
        ImageArray: should be a numpy array
        Time: Number of seconds the frames to be rendered
        Frames: Number of frames per second
    Image Array can be either be three channel or four channel (RGB or RGBA)
    Return:
         Returns a Stack of Image array
         Image array will be four channel
    """
    Height = len(ImageArray)
    Width = len(ImageArray[0])
    Channel = len(ImageArray[0][0])
    Stack = []
    MaxRadius = sqrt((Height * Height) / 4 + (Width * Width) / 4)
    CenterCoordinates = (int(Width / 2), int(Height / 2))
    Color = (0, 0, 0, 0)
    Thickness = -1
    if Channel == 3:
        ImageArray = RGB2RGBA(ImageArray)
    for i in range(Time * Frames):
        Rad = int((MaxRadius / (Time * Frames)) * (i + 1))
        image = circle(ImageArray, CenterCoordinates, Rad, Color, Thickness)

        Stack.append(image)

    Stack.reverse()
    return Stack
