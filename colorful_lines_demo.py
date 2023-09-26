import simpleguitk as simplegui
import numpy as np

import math
import random

bounce_border = 0.1
speed_co = 0.3

max_vel = 3

frame_width = 500

#if you set drift to false, then you can control the direction the 
#lines point using your mouse by clicking and holding down
drift = True

poi = [frame_width/2,frame_width/2]

max_line = 30

points = []

num_points = 256 # perfect squares only, 4,16,25...256,400,900 etc

def rgb_to_hex(r, g, b):
    # print(f"{r}, {g}, {b}")
    # print('#{:02x}{:02x}{:02x}'.format(r, g, b))
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

class point():
    x=0
    y=0
    xvel=0
    yvel=0
    
    red = 255
    green = 255
    blue = 255
    
    color = f"rgb({red},{green},{blue})"
    
    close = [x,y]
    far = [-x,-y]
    
    dis_poi = 0
    
    def __init__(this,x,y,xvel,yvel):
        this.x = x
        this.y=y
        this.xvel = xvel
        this.yvel = yvel
    def getPos(this):
        return [this.x,this.y]
    def updateLines(this):
        
        poi_x = poi[0]
        poi_y = poi[1]
        
        x = this.x
        y = this.y
        
        row_col = int(math.sqrt(num_points))
        border = frame_width/(row_col+1) 
        
        line_len = max_line/2
        
        dis_poi = math.sqrt((x-poi_x)**2+(y-poi_y)**2)
        ratio = 1-dis_poi/math.sqrt((frame_width-2*border)**2+(frame_width-2*border)**2)
        if (dis_poi<ratio*line_len):
            line_len = dis_poi
        
        tot_x_diff = (x-poi_x)
        tot_y_diff = (y-poi_y)
        
        #print("this.x:",this.x," this.y:",this.y,"poi_x:",poi_x,"poi_y",poi_y)
        
        theta = math.atan(tot_y_diff/tot_x_diff)
        
        close_x = (ratio*line_len)*math.cos(theta)
        close_y = (ratio*line_len)*math.sin(theta)
        
        #print("tot_x_diff:",tot_x_diff,"tot_y_diff",tot_y_diff,"theta:",theta,"close_x:",close_x,"close_y:",close_y)
        
        this.close = [close_x+x,close_y+y]
        this.far = [-close_x+x,-close_y+y]
        
        r = ratio*255
        g = (1-ratio)*200-50
        b = (1-ratio)*255
        this.red = min(max(int(r),0),255)
        this.green = min(max(int(g),0),255)
        this.blue = min(max(int(b),0),255)



        this.color = rgb_to_hex(this.red,this.green,this.blue)

        #this.color = f"rgb({r},{g},{b})"
        

def makepoints():
    global points
    row_col = int(math.sqrt(num_points))
    y_spacing = frame_width/(row_col+1)
    x_spacing = frame_width/(row_col+1)
    for i in range(row_col):
        for j in range(row_col):
            temp = point((i+1)*x_spacing,(j+1)*y_spacing,0,0)
            points.append(temp)           
            
def drawpoints(canvas):
    #canvas.draw_point(poi,"red")
    for i in points:
        #canvas.draw_point(i.getPos(),"white")
        # print(f"{i.red}, {i.green}, {i.blue}")
        # print(i.color)
        canvas.draw_line(i.close,i.far,1,i.color)
        canvas.draw_circle(i.far,1,2,i.color,i.color)
        canvas.draw_circle(i.close,1,2,i.color,i.color)

        
#onetime code:

def updatepoints():
    global points
    for i in points:
        i.updateLines()

makepoints()

class drifter():
    xvel=0
    yvel=0
    def __init__(this,xvel,yvel):
        this.xvel = xvel
        this.yvel = yvel
    def updateDrift(this):
        global poi
        poi_x = poi[0]
        poi_y = poi[1]
        
        xvel = this.xvel
        yvel = this.yvel
        
        poi[0] +=xvel
        poi[1] +=yvel
        
        send = True
        
        if (poi_x>=frame_width-bounce_border*frame_width):
            this.xvel-=speed_co
            send = False
        if (poi_x<=bounce_border*frame_width):
            this.xvel+=speed_co
            send = False
        if (poi_y>=frame_width-bounce_border*frame_width):
            this.yvel-=speed_co
            send = False
        if (poi_y<=bounce_border*frame_width):
            this.yvel += speed_co
            send = False
        
        if send:
            this.xvel+=random.randint(-1,1)*(speed_co)
            this.yvel+=random.randint(-1,1)*(speed_co)
            
        this.xvel = min(max_vel,this.xvel)
        this.yvel = min(max_vel,this.yvel)
            
    
dr = drifter(0,0)
# Handler to draw on canvas
def draw(canvas):
    global dr
    updatepoints()
    drawpoints(canvas)
    if drift:
        dr.updateDrift()

def mouse_handler(position):
    global poi
    if not drift:
        poi = position

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", frame_width, frame_width)
frame.set_draw_handler(draw)
frame.set_mousedrag_handler(mouse_handler)

# Start the frame animation
frame.start()
