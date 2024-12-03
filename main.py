import pygame as pg
import sys
import obj3d
import cam
import numpy as np
import math

try:
    from numba import njit
except ModuleNotFoundError:
    print("can't use njit")
    def checkBoarder(p,w,h):
        return not np.any((p > w) | (p > h))
else:
    @njit
    def checkBoarder(p,w,h):
        return not np.any((p > w) | (p > h))

class Main:
    def __init__(self):
        self.reso=self.width,self.height=1200,1200
        self.hw=self.width/2
        self.hh=self.height/2
        pg.init()
        self.scr=pg.display.set_mode(self.reso)
        pg.display.set_caption("3d")
        self.contraling=[]

        self.obj=obj3d.Tesseract(self)
        self.cam=cam.Cam(self)
        self.setUpProjectionM()
        self.NDCtoScr=np.array((         # copied
            (self.hw,0,0,0),
            (0,-self.hh,0,0),
            (0,0,1,0),
            (self.hw,self.hh,0,1)
        ))
        
        self.clock=pg.time.Clock()
        self.font=pg.font.Font(None,self.height//20)
        self.fps=60
        self.main()

    def setUpProjectionM(self):         # copied
        near,far=0.01,1000

        h_vol=math.pi/3
        v_vol=h_vol*(self.height/self.width)

        right=math.tan(h_vol/2)
        top=math.tan(v_vol/2)
        left,bottom=-right,-top

        m00=2/(right-left)
        m11=2/(top-bottom)
        m22=(far+near)/(far-near)
        m32=-2*near*far/(far-near)

        self.projectionM=np.array([
            (m00,0,0,0),
            (0,m11,0,0),
            (0,0,m22,1),
            (0,0,m32,0)
        ])
        


    def display(self,v):
        v=v@self.cam.camMatrix()
        # move it in front of camera
        v=v@self.projectionM
        # move into clip space
        v /= v[:,-1].reshape(-1,1)
        # normalize
        v=v@self.NDCtoScr
        # from ndc space to window
        v=v[:,:2]
        # take x and y
        return v

    def main(self): 
        while 1:
            self.checkEvent()
            self.scr.fill((40,70,70))
            self.obj.update()
            points=self.obj.vertexes()
            points=self.display(points)
            faces=self.obj.faces()
            for i in faces:
                for v in faces[i]:
                    polygon=points[v]
                    pg.draw.polygon(self.scr,(255,255,255),polygon,int(self.hh/256))
            #for i in points:
            #    if checkBoarder(i,self.height,self.width):
            #        pg.draw.circle(self.scr,(0,255,0),i,self.height//256)
            self.scr.blit(self.font.render(str(self.clock.get_fps()),False,(255,255,255)),(0,0))
            pg.display.flip()
            self.clock.tick(self.fps)
#

    def checkEvent(self):
        for e in pg.event.get():
            if e.type==pg.QUIT:
                sys.exit()
            if e.type==pg.KEYDOWN:
                self.contraling.append(e.key)
            if e.type==pg.KEYUP and e.key in self.contraling:
                self.contraling.remove(e.key)
        for e in self.contraling:
            self.cam.contral(e)

Main()