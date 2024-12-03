import numpy as np
from trantrix import *

class ThreeD:
    def __init__(self,vertexes,faces):
        w=np.array([1 for i in range(len(vertexes))])
        self.vertexes=np.column_stack((vertexes,w))
        self.faces=faces

    def translate(self, pos):
        self.vertexes=self.vertexes @ translate(pos)
    def scale(self, new_scale):
        self.vertexes=self.vertexes @ scale(new_scale)
    def rotate_x(self, angle):
        self.vertexes=self.vertexes @ rotate_x(angle)
    def rotate_y(self, angle):
        self.vertexes=self.vertexes @ rotate_y(angle)
    def rotate_z(self, angle):
        self.vertexes=self.vertexes @ rotate_z(angle)



class Tesseract:
    def __init__(self,game):
        self.game=game
        self.updateSequ=0
        self.moveSpeed=0.005
        self.scaleSpeed=0.005
        outer0v=np.array(((-2, 2, -2), (-2, 2, 2), (-2, -2, 2), (-2, -2, -2)))
        inner0v=np.array(((-1, 1, -1), (-1, 1, 1), (-1, -1, 1), (-1, -1, -1)))
        inner1v=np.array(((1, 1, -1), (1, 1, 1), (1, -1, 1), (1, -1, -1)))
        outer1v=np.array(((2, 2, -2), (2, 2, 2), (2, -2, 2), (2, -2, -2)))
        faces=np.array([i for i in range(4)])
        self.squares=[ThreeD(outer0v,faces),ThreeD(inner0v,faces),ThreeD(inner1v,faces),ThreeD(outer1v,faces)]
        self.midSquareDir=1
        self.squareMove=0
        self.connect3dOut=np.array([[i,12+i] for i in range(4)])
        self.connect3dIut=np.array([[4+i,8+i] for i in range(4)])
        self.connect4d=np.array([[4*(2*j)+i, 4*(2*j+1)+i] for j in range (2) for i in range(4)])

    def update(self):
        if self.squares[(self.squareMove+3)%4].vertexes[0][0]>=2 or self.squares[self.squareMove].vertexes[0][0]<=-2:
            self.squareMove-=1
            self.squareMove%=4
            self.midSquareDir=1
        
        index=self.squareMove
        before0=self.squares[index].vertexes[0][0]
        self.squares[index].translate((-self.moveSpeed*4,0,0))
        self.scale(self.squares[index].vertexes,self.midSquareDir,self.scaleSpeed/8)
        if before0>0 and self.squares[index].vertexes[0][0]<0:self.midSquareDir=-1

        index+=1
        self.squares[index%4].translate((self.moveSpeed,0,0,))
        self.scale(self.squares[index%4].vertexes,-1,self.scaleSpeed)

        index+=1
        self.squares[index%4].translate((self.moveSpeed*2,0,0,))

        index+=1
        self.squares[index%4].translate((self.moveSpeed,0,0,))
        self.scale(self.squares[index%4].vertexes,1,self.scaleSpeed)


    def scale(self,vertexes,dire,speed):
        vertexes[:,1:3]+=vertexes[:,1:3]*(dire*speed)
        return vertexes
               

    def vertexes(self):
        points=[]
        for i in self.squares:
            points.extend(i.vertexes.tolist())
        return np.array(points)

    def faces(self):
        returns={
            (255,0,0):(self.squares[1].faces+4,self.squares[2].faces+8,*self.connect3dIut),
            (0,255,0):self.connect4d,
            (0,0,255):(self.squares[0].faces,self.squares[3].faces+12,*self.connect3dOut)
        }
        return returns