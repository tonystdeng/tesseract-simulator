import numpy as np
import pygame as pg
from trantrix import *

class Cam:
    def __init__(self,game,pos=(0.,0.,-20.,0.)):
        self.pos=np.array(pos)
        self.game=game
        self.forward=np.array([0.,0.,1.,1.]) #copied
        self.up=np.array([0.,1.,0.,1.])      #copied
        self.right=np.array([1.,0.,0.,1.])   #copied
        self.angles=[0,0,0]
        self.move_speed=0.2
        self.rotate_speed=0.01
    
    def camMatrix(self):
        x,y,z,w=self.pos
        trans=np.array([
            [1,0,0,0],
            [0,1,0,1],
            [0,0,1,0],
            [-x,-y,-z ,1]
        ])
        rx,ry,rz,w=self.right
        ux,uy,uz,w=self.up
        fx,fy,fz,w=self.forward
        rotate=np.array([
            [rx,ux,fx,0],
            [ry,uy,fy,0],
            [rz,uz,fz,0],
            [0,0,0,1]
        ])
        return trans@rotate

    def contral(self,e):
        if e==pg.K_a:
            self.pos-=self.right * self.move_speed
        if e==pg.K_d:
            self.pos+=self.right * self.move_speed
        if e==pg.K_s:
            self.pos-=self.forward * self.move_speed
        if e==pg.K_w:
            self.pos+=self.forward * self.move_speed
        if e==pg.K_q:
            self.pos-=self.up * self.move_speed
        if e==pg.K_e:
            self.pos+=self.up * self.move_speed
        if e==pg.K_LEFT:
            self.rotate_y(-self.rotate_speed)
        if e==pg.K_RIGHT:
            self.rotate_y(self.rotate_speed)
        if e==pg.K_UP:
            self.rotate_x(-self.rotate_speed)
        if e==pg.K_DOWN:
            self.rotate_x(self.rotate_speed)

    def rotate_y(self,angle):
        self.angles[1]+=angle
        rotate=rotate_y(angle)
        self.forward =self.forward @ rotate
        self.up =self.up @ rotate
        self.right =self.right @ rotate

    def rotate_x(self,angle):
        self.angles[0]+=angle
        rotate=rotate_x(angle)
        self.forward =self.forward @ rotate
        self.up =self.up @ rotate
        self.right =self.right @ rotate

    def rotate_z(self,angle):
        self.angles[2]+=angle
        rotate=rotate_z(angle)
        self.forward =self.forward @ rotate
        self.up =self.up @ rotate
        self.right =self.right @ rotate
    