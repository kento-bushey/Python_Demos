import simpleguitk as simplegui
import math
import numpy as np

plane_offset = -35
speed = 0.5 # speed of rotation if you want it to rotate

x_sensitivity = 1 #0-1, 1 is more sensitive
y_sensitivity = 1

def cos(theta):
    return math.cos(math.radians(theta))
def sin(theta):
    return math.sin(math.radians(theta))

focal_length = 1000

#axis:
x_axis = (1,0,0)
y_axis = (0,1,0)
z_axis = (0,0,1)

#rotate Scene around this axis:
scene_axis = (0,cos(plane_offset),sin(plane_offset))

frame_width = 400

timer = 0

def rgb_to_hex(color):
    return '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])
class point():
    def __init__(this,x,y, z):
        this.x=x
        this.y=y
        this.z = z
    def __str__(this):
        return f"({int(this.x)}, {int(this.y)}, {int(this.z)})"
    def getpos(this,):
        return [-this.x+frame_width/2,-this.y+frame_width/2]
    def getz(this):
        return this.z
    def rotate_point_around_axis(this, axis, degrees):
        x1 = this.x
        y1 = this.y
        z1 = this.z
        u1,u2,u3 = axis[0],axis[1],axis[2]
        # Convert degrees to radians
        radians_angle = math.radians(degrees)

        # Normalize the axis vector to ensure it's a unit vector
        axis_length = np.sqrt(u1**2 + u2**2 + u3**2)
        u1 /= axis_length
        u2 /= axis_length
        u3 /= axis_length

        # Construct the rotation matrix for the given axis and angle
        c = math.cos(radians_angle)
        s = math.sin(radians_angle)
        rotation_matrix = np.array([[u1*u1*(1-c)+c,   u1*u2*(1-c)-u3*s, u1*u3*(1-c)+u2*s],
                                    [u2*u1*(1-c)+u3*s, u2*u2*(1-c)+c,   u2*u3*(1-c)-u1*s],
                                    [u3*u1*(1-c)-u2*s, u3*u2*(1-c)+u1*s, u3*u3*(1-c)+c]])

        # Apply the rotation matrix to the input point
        input_point = np.array([x1, y1, z1])
        rotated_point = np.dot(rotation_matrix, input_point)
        this.x = rotated_point[0]
        this.y = rotated_point[1]
        this.z = rotated_point[2]
        return rotated_point
    def project(this):
        """Perform perspective projection on the point"""
        if this.z != 0:
            scale_factor = focal_length / (focal_length + this.z)
            return (this.x * scale_factor+frame_width/2, -this.y * scale_factor+frame_width/2)
        else:
            # Avoid division by zero
            return (frame_width/2+this.x, frame_width/2+this.y)

class face():
    points = []
    color = "blue"
    def __init__(this,points,color):
        this.points = points
        this.color=color

class rectangularPrism():
    faces = []
    def __init__(this, pos,xlen,ywid,zhei,color):
        x = pos[0]
        y = pos[1]
        z = pos[2]
        this.pos = point(x,y,z)

        lenRad = xlen/2
        widRad = ywid/2
        heiRad = zhei/2

        p1 = point(x+lenRad,y+widRad,z+heiRad) #
        p2 = point(x+lenRad,y-widRad,z+heiRad) # These are the far face
        p3 = point(x-lenRad,y-widRad,z+heiRad) # 
        p4 = point(x-lenRad,y+widRad,z+heiRad) #

        p5 = point(x+lenRad,y+widRad,z-heiRad) #
        p6 = point(x+lenRad,y-widRad,z-heiRad) # These are the close face
        p7 = point(x-lenRad,y-widRad,z-heiRad) # 
        p8 = point(x-lenRad,y+widRad,z-heiRad) #

        far = face([p1,p2,p3,p4],color)
        close = face([p5,p6,p7,p8],color)
        right = face([p1,p2,p6,p5],color)
        left = face([p4,p3,p7,p8],color)
        top = face([p1,p4,p8,p5],color)
        bottom = face([p2,p3,p7,p6],color)
        
        this.points = [p1,p2,p3,p4,p5,p6,p7,p8]
        this.faces = [far,close,right,left,top,bottom]
        
        # bottom_triangles = split_face_into_triangles(bottom)
        # for i in bottom_triangles:
        #     this.faces.append(i)
    def getPos(this):
        return (this.pos)
    def getFaces(this):
        return this.faces
    def getClosestPoint(this):
        sorted_points = sorted(this.points, key=lambda p: (p.z+frame_width/2)**2 + p.x**2 + p.y**2, reverse=True)
        p = sorted_points[0]
        return (p.z+frame_width/2)**2 + p.x**2 + p.y**2

class pyramid():
    def __init__(this, pos,xlen,ywid,zhei,color):
        x = pos[0]
        y = pos[1]
        z = pos[2]
        this.pos = point(x,y,z)

        lenRad = xlen/2
        widRad = ywid/2
        heiRad = zhei/2

        p1 = point(x,y+widRad,z)
        p2 = point(x-lenRad,y-widRad,z-heiRad)
        p3 = point(x-lenRad,y-widRad,z-heiRad)

        faces = face(p1,p2,p3)

def sort(face_list):
    #sorted_faces = sorted(face_list, key=lambda face: sum((((p.z+frame_width/2)**2)+p.x**2+p.y**2) for p in face.points) / len(face.points), reverse=True)
    sorted_faces = sorted(face_list, key=lambda face: min(frame_width/2-(p.z) for p in face.points), reverse=False)
    return sorted_faces

def drawFaces(canvas, face_list):
    sorted_faces = sort(face_list)

    for i in range(len(sorted_faces)):
        ratio = 0.7
        line_color = rgb_to_hex([int(sorted_faces[i].color[0]*ratio),int(sorted_faces[i].color[1]*ratio),int(sorted_faces[i].color[2]*ratio)])
        face_color = rgb_to_hex(sorted_faces[i].color)
        projected_coords = [p.project() for p in sorted_faces[i].points]
        if i == len(sorted_faces) - 1:
            canvas.draw_polygon(projected_coords, 1, line_color, face_color)
        else:
            canvas.draw_polygon(projected_coords, 1, line_color, face_color)

def rotatePointsAxis(points,axis,degrees):
    for i in points:
        i.rotate_point_around_axis(axis,degrees)

def split_face_into_triangles(face_object):
    # Get the points of the original face
    points = face_object.points

    num_points = len(points)

    # Calculate the center point of the face
    center_x = sum(p.x for p in points) / num_points
    center_y = sum(p.y for p in points) / num_points
    center_z = sum(p.z for p in points) / num_points
    center_point = point(center_x, center_y, center_z)

    # Create new faces representing the triangles
    triangles = []
    for i in range(num_points):
        triangle = face([points[i], points[(i + 1) % num_points], center_point], face_object.color)
        triangles.append(triangle)

    return triangles

def rotateScene(scene,axis,degrees):
    for i in scene:
        rotatePointsAxis(i.points,axis,degrees)

def draw_handler(canvas):
    global timer
    timer+=1
    manageScene(canvas,scene)

def sortScene(scene):
    sorted_shapes = sorted(scene, key=lambda shape: shape.getClosestPoint(), reverse=True)
    return sorted_shapes

def drawScene(canvas,scene):
    face_list = []
    for i in scene:
        face_list+= i.faces
    drawFaces(canvas,face_list)

def manageScene(canvas,scene):
    if timer == 1:
        rotateScene(scene,(1,0,0),plane_offset)
    #rotateScene(scene,scene_axis,speed)
    drawScene(canvas,scene)

last_pos = []
last_time = 0

def mouse_handler(position):
    global last_pos,last_time
    if last_pos == [] or abs(timer-last_time)>2:
        last_pos = position
    x_change = position[0] - last_pos[0]
    y_change = position[1] - last_pos[1]

    rotateScene(scene,x_axis,(-y_change*(5*y_sensitivity))*speed)
    rotateScene(scene,scene_axis,(-x_change*(5*x_sensitivity))*speed)

    last_time = timer
    last_pos = position
    
house = rectangularPrism([20,20,0],40,40,40,(150,110,150))
shed = rectangularPrism([-10,30,-10],20,60,20,(150,15,15))
shed2 = rectangularPrism([-20,10,20],40,20,40,(15,15,150))
floor = rectangularPrism([0,-5,0],120,10,120,(50,110,50))

scene = [house,shed,floor,shed2]

frame = simplegui.create_frame('Frame', 400, 400)
frame.set_draw_handler(draw_handler)
frame.set_mousedrag_handler(mouse_handler)
frame.start()