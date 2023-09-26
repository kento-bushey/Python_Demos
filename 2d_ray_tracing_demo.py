import simpleguitk as simplegui
import math

frame_width = 400
ray_increment = 0.5
dist = 350
speed = 0.1

draw_rays = False

sun_height = 200

def cos(theta):
    return math.cos(math.radians(theta))
def sin(theta):
    return math.sin(math.radians(theta))

def rot(x,y,angle):
    New_x = x * cos(angle) + y * sin(angle) 
    New_y = (-x) * sin(angle) + y * cos(angle)
    return [New_x,New_y]

def rgb_to_hex(color):
    # print(f"{r}, {g}, {b}")
    # print('#{:02x}{:02x}{:02x}'.format(r, g, b))
    return '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])

def shadow(color):
    r = color[0]
    g = color[1]
    b = color[2]
    shadowval = 0.3
    return max(0,int(int(r)*shadowval)), max(0,int(int(g)*shadowval)),max(0,int(int(b)*shadowval))

class source():
    radius = 10
    color = [255,255,255]
    line_len = dist
    x = 200
    y = 200
    def __init__(this,x,y,color):
        this.x=x
        this.y=y
        this.color = color
    def drawSource(this,canvas):
        #canvas.draw_circle([this.x,this.y],this.radius*20,1,rgb_to_hex(shadow(shadow(this.color))),rgb_to_hex(shadow(shadow(this.color))))
        canvas.draw_circle([this.x,this.y],this.radius,1,rgb_to_hex(this.color),rgb_to_hex(this.color))
    def getPos(this):
        return [this.x,this.y]
    def getRays(this):
        raylist = []
        line_len = this.line_len
        for i in range(int(360/ray_increment)):
            p = [ line_len*math.cos(math.radians(i*ray_increment+0.001)) +this.x, line_len*math.sin(math.radians(i*ray_increment+0.001))+this.y]
            raylist.append(p)
        return raylist

class point():
    def __init__(this,x,y):
        this.x=x
        this.y=y
    def getPoints(this):
        return [this.x,this.y]

class face():
    def __init__(this,points,color = [255,255,255]):
        this.points = points
        this.color = color
    def getPoints(this):
        return [this.points[0],this.points[1]]
    def drawFace(this,canvas):
        canvas.draw_line(this.points[0].getPoints(),this.points[1].getPoints(),1,rgb_to_hex(shadow(this.color)))
    
def drawRays(source,canvas,intersects):
    raylist = source.getRays()
    origin = source.getPos()
    for i in raylist:
        canvas.draw_line(origin,i,0.1,rgb_to_hex([100,100,20]))

def find_intersection(line1, line2):
    x1, y1 = line1[0]
    x2, y2 = line1[1]
    a1, b1 = line2[0]
    a2, b2 = line2[1]

    # Check if line1 is vertical
    if x1 == x2:
        # Check if line2 is also vertical (parallel)
        if a1 == a2 and x1 == a1:
            # Lines are collinear and overlap
            y_min1, y_max1 = min(y1, y2), max(y1, y2)
            y_min2, y_max2 = min(b1, b2), max(b1, b2)

            if y_max1 < y_min2 or y_max2 < y_min1:
                return "Parallel"  # No intersection
            else:
                return "Collinear"

        # Calculate the x-coordinate of the intersection point
        x_int = x1
        # Use the equation of line2 to find the y-coordinate
        m2 = (b2 - b1) / (a2 - a1) if a2 - a1 != 0 else float('inf')  # Avoid division by zero
        c2 = b1 - m2 * a1
        y_int = m2 * x_int + c2
    else:
        # Check if line2 is vertical
        if a1 == a2:
            # Calculate the x-coordinate of the intersection point
            x_int = a1
            # Use the equation of line1 to find the y-coordinate
            m1 = (y2 - y1) / (x2 - x1)
            c1 = y1 - m1 * x1
            y_int = m1 * x_int + c1
        else:
            # Calculate the slopes and y-intercepts of the two lines
            m1 = (y2 - y1) / (x2 - x1)
            c1 = y1 - m1 * x1

            m2 = (b2 - b1) / (a2 - a1) if a2 - a1 != 0 else float('inf')  # Avoid division by zero
            c2 = b1 - m2 * a1

            # Check if the lines are parallel (or collinear)
            if m1 == m2:
                # Check if the lines overlap (collinear)
                if c1 == c2:
                    return "Collinear"
                else:
                    return "Parallel"

            # Calculate the point of intersection
            x_int = (c2 - c1) / (m1 - m2)
            y_int = m1 * x_int + c1

    # Check if the intersection point is within the range of both lines
    if (
        min(x1, x2) <= x_int <= max(x1, x2) and min(y1, y2) <= y_int <= max(y1, y2) and
        min(a1, a2) <= x_int <= max(a1, a2) and min(b1, b2) <= y_int <= max(b1, b2)
    ):
        return (x_int, y_int)
    else:
        return "Out of bounds"


def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

def drawIntersects(source):
    raylist = source.getRays()
    origin = source.getPos()
    intersectList = []
    drawlist = []
    for i in raylist:
        rayIntersects = []
        small = float('inf')
        smallest = []
        for j in faceList: 
            ray = [origin,i]
            #print("ray: "+str(ray[0])+str(ray[1]))
            surface = [j.getPoints()[0].getPoints(),j.getPoints()[1].getPoints()]
            #print(surface)
            intersect = find_intersection(ray, surface)
            if type(intersect)!= str:
                dist = calculate_distance(origin,intersect)
                if dist<small:
                    smallest = [intersect,j.color]
                    small = dist
                rayIntersects.append(intersect)
            #drawlist.append(ray)
        if smallest != []:
            intersectList.append(smallest)
            drawlist.append([origin,smallest[0]])
        else:
            drawlist.append(ray)
    if (origin[1]>500):
        return [[intersectList[0]],[drawlist[0]]]
    return [intersectList,drawlist]

def draw_env(canvas):
    for i in faceList:
        i.drawFace(canvas)

leftRoof = face([point(220,310),point(251.1,290)],[128,109,79])
rightRoof = face([point(280,310),point(249.9,290)],[128,109,79])
rightWall = face([point(275,307),point(275.1,350)],[128,70,27])
leftWall = face([point(225,307),point(225.1,350)],[128,70,27])
floor = face([point(-1,350.05),point(401.05,350.06)],[0,200,0])

leftTreeStump = face([point(115,325),point(115.1,350)],[110,60,0])
rightTreeStump = face([point(120,325),point(120.1,350)],[110,60,0])
treeLeavesBase = face([point(105,325),point(130,325)],[0,250,0])
treeLeavesLeft = face([point(105,325),point(117.5,250)],[0,250,0])
treeLeavesRight = face([point(130,325),point(117.5,250)],[0,250,0])

leftBorder = face([point(-1,349),point(-1.1,401)],[0,0,0])
rightBorder = face([point(400.1,349),point(400.05,402)],[0,0,0])
bottomBorder = face([point(-2,400.1),point(402,400)],[0,0,0])


faceList = [leftRoof,rightRoof,rightWall,leftWall,floor, leftTreeStump,rightTreeStump, treeLeavesLeft, treeLeavesBase, treeLeavesRight, leftBorder,rightBorder,bottomBorder]

arcradius = 300

sun = source(200,400-arcradius,[255,255,0])
moon = source(200,400+arcradius,[255,255,255])

def updateSource(speed):
    xy = rot(sun.x-200,sun.y-400,speed)
    sun.x = xy[0]+200
    sun.y = xy[1]+400
    xy = rot(moon.x-200,moon.y-400,speed)
    moon.x = xy[0]+200
    moon.y = xy[1]+400

def draw(canvas):

    updateSource(speed) # speed
    
    sun.drawSource(canvas)
    moon.drawSource(canvas)

    sun_intersects = drawIntersects(sun)
    moon_intersects = drawIntersects(moon)

    intersects  = sun_intersects[0]+moon_intersects[0]
    drawl = sun_intersects[1] + moon_intersects[1]
    if (draw_rays):

        for b in drawl: # draw rays of light
            canvas.draw_line(b[0],b[1],0.1,rgb_to_hex([50,50,50]))

    draw_env(canvas)

    #print("\n"+str(intersects))
    for i in intersects: # draw points of light
        canvas.draw_circle(i[0],0.7,1.2,rgb_to_hex(i[1]))

    #drawRays(canvas)

frame = simplegui.create_frame("Home", frame_width, frame_width)
frame.set_draw_handler(draw)

frame.start()