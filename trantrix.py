import math
import numpy as np

def translate(point):
    tx,ty,tz=point
    return np.array([
        [1, 0, 0, 0 ],
        [0, 1, 0, 0 ],
        [0, 0, 1, 0 ],
        [tx,ty,tz,1 ]
    ])

def rotate_x(angle):
    return np.array([
        [1, 0, 0, 0],
        [0, math.cos(angle), math.sin(angle), 0],
        [0, -math.sin(angle), math.cos(angle), 0],
        [0, 0, 0, 1]
    ])

def rotate_y(angle):
    return np.array([
        [math.cos(angle), 0, -math.sin(angle), 0],
        [0, 1, 0, 0],
        [math.sin(angle), 0, math.cos(angle), 0],
        [0, 0, 0, 1]
    ])

def rotate_z(angle):
    return np.array([
        [math.cos(angle), math.sin(angle), 0, 0],
        [-math.sin(angle), math.cos(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def scale(n):
    return np.array([
        [n, 0, 0, 0 ],
        [0, n, 0, 0 ],
        [0, 0, n, 0 ],
        [0, 0, 0, 1 ]
    ])