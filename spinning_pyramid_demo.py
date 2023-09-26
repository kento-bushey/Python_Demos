import simpleguitk as simplegui
import math
import random

drawgrid = False

xyOffset = 20
zyOffset = 0
xzOffset = 0

xyrotation = 0
zyrotation = 0
xzrotation = 1

angle_increment = -1

colors = ["red", "yellow", "green", "blue", "pink"]
def randColor():
    return colors[random.randint(0,len(colors)-1)]

def cos(theta):
    return math.cos(math.radians(theta))
def sin(theta):
    return math.sin(math.radians(theta))
#rotates all points around the axiz z (can be generalized)
def rot(x,y,angle):
    New_x = x * cos(angle) + y * sin(angle) 
    New_y = (-x) * sin(angle) + y * cos(angle)
    return [New_x,New_y]

class point():
    def __init__(this,x,y, z):
        this.x=x
        this.y=y
        this.z = z
    def __str__(this):
        return f"({int(this.x)}, {int(this.y)}, {int(this.z)})"
    def rotatexy(this,angle):
        xyvals = rot(this.x,this.y,angle)
        this.x = xyvals[0]
        this.y = xyvals[1]
    def rotatezy(this,angle):
        xyvals = rot(this.z,this.y,angle)
        this.z = xyvals[0]
        this.y = xyvals[1]
    def rotatexz(this,angle):
        xyvals = rot(this.x,this.z,angle)
        this.x = xyvals[0]
        this.z = xyvals[1]
    def getpos(this,):
        return [-this.x+200,-this.y+200]
    def getz(this):
        return this.z
    
def drawgrid(canvas):
    canvas.draw_line([200,0],[200,400],1,"red")
    canvas.draw_line([0,200],[400,200],1,"red")
        
    
def drawPoint(canvas, plist,variance):
    inc = 10
    for p in range(len(plist)):
        if (p==0):
            canvas.draw_circle(plist[p].getpos(),3,6,"yellow")
        else:
            canvas.draw_circle(plist[p].getpos(),3,6,"red")
        canvas.draw_text((plist[p].__str__()),(300,10+inc),12,"white")
        inc+=variance
    
def connectLines(canvas,points):
    for i in range(len(points)):
        if (i == len(points)-1):
            canvas.draw_line(points[i].getpos(), points[0].getpos(),3,"red")
        else:
            canvas.draw_line(points[i].getpos(), points[i+1].getpos(),3,"red")
            

            
#triangle coords

class face():
    points = []
    color = "blue"
    def __init__(this,points,color):
        this.points = points
        this.color=color
    
        
p1 = point(-50,50,-25)
p2 = point(-50,-50,-25)
p3 = point(50,0,-25)

#
py1 = point(-50,-50,50)
py2 = point(50,-50,50)
py3 = point(-50,-50,-50)
py4 = point(50,-50,-50)
py5 = point(0,50,0)

face1 = face([py1,py2,py4,py3],"navy")
face2 = face([py1,py2,py5],"navy")
face3 = face([py2,py4,py5],"navy")
face4 = face([py4,py3,py5],"navy")
face5 = face([py3,py1,py5],"navy")

shape = [face1,face2,face3,face4,face5]

#faces = [[py1,py2,py4,py3],[py1,py2,py5],[py2,py4,py5],[py4,py3,py5],[py3,py1,py5]]
pyface_colors = ["blue","blue","blue","blue","blue"]

def pyfaceCoords(facelist,index):
    ret = []
    for i in facelist[index].points:
        ret.append(i.getpos())
    return ret

def sort(faces):
    sorted_faces = sorted(faces, key=lambda face: sum(point.z for point in face.points) / len(face.points))
    return sorted_faces

#temp = sort(faces)

def drawFaces(canvas, points):
    pointlist = sort(points)
    for i in range(len(points)):
        canvas.draw_polygon(pyfaceCoords(pointlist,i),1,"white",shape[i].color)
    


def rotatePoints(points,anglexy, anglezy, anglexz):
    for i in points:
        i.rotatezy(anglezy)
        i.rotatexy(anglexy)
        i.rotatexz(anglexz)

def triangle(canvas):
    pointlist = [p1,p2,p3]
    drawPoint(canvas,pointlist,12)
    rotatePoints(pointlist,0.5,0.2,0)
    connectLines(canvas,pointlist)
    
def pyramid(canvas, time):
    
    if time ==1:
       rotatePoints([py1,py2,py3,py4,py5],xyOffset,zyOffset,xzOffset)
    
    points = [py1,py2,py3,py4,py5]
    
    connectLines(canvas,[py1,py2,py4,py3])
    connectLines(canvas,[py1,py2,py5])
    connectLines(canvas,[py3,py4,py5])
    
    drawPoint(canvas,points,12)
    #degrees on the planes (xy, zy, xz) 
    rotatePoints(points,xyrotation,zyrotation,xzrotation)
    
    drawFaces(canvas,shape)

timer = 1
    
def draw_handler(canvas):
    global timer
    canvas.draw_circle((200,200),2,4,"red")
    pyramid(canvas,timer)
    timer+=1
    #if (drawgrid):
        #drawgrid(canvas)

frame = simplegui.create_frame('Testing', 400, 400)
frame.set_draw_handler(draw_handler)
frame.start()
#________________________
