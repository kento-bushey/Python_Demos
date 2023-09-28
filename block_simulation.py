import simpleguitk as simplegui

# Constants
WIDTH = 500
HEIGHT = 500

collisions = 0

def rgb_to_hex(color):
    return '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])

class block():
    def __init__(this,position,side_length, weight,vel, color = [255,255,255],movable = True):
        this.side_length = side_length
        this.mass = weight
        this.x = position
        this.vel = vel
        this.color = color
        this.is_movable = movable
    def draw_block(this,canvas):
        rad = this.side_length/2
        xoffset = boundary[0]
        yoffset = boundary[1]
        canvas.draw_polygon([[this.x-rad+xoffset,rad+yoffset-rad],[this.x-rad+xoffset,-rad+yoffset-rad],[this.x+rad+xoffset,-rad+yoffset-rad],[this.x+rad+xoffset,rad+yoffset-rad]],1,"white",rgb_to_hex(this.color))
    def update(self): #obselete
        self.x += self.vel
def check_collision(block1, block2):
    global collisions
    distance = block2.x - block1.x
    if distance <= (block1.side_length + block2.side_length) / 2:
        # Collision occurred, now calculate the new velocities
        v1_final = ((block1.mass - block2.mass) * block1.vel + 2 * block2.mass * block2.vel) / (block1.mass + block2.mass)
        v2_final = ((block2.mass - block1.mass) * block2.vel + 2 * block1.mass * block1.vel) / (block1.mass + block2.mass)
        #block1.vel = v1_final
        #block2.vel = v2_final
        collisions+=1

        return [v1_final,v2_final]
    return [block1.vel,block2.vel]

def sub_update(update_count):
    for i in range(update_count):
        check_all_collision()
        for i in block_list:
            i.update()

block1 = block(100,20,1,0)
block2 = block(200,40,10**8,-0.00007)
boundary_block= block(-10,20,2**62,0,[10,10,10],False)

block_list = [block1,block2,boundary_block]
boundary = [100,400]

def drawArena(canvas):
    canvas.draw_polyline([[boundary[0],boundary[1]/4],boundary,[boundary[0]*4,boundary[1]]],2,"white")
def check_all_collision():
    block_pairs = [[block1,block2],[boundary_block,block1]]
    for i in block_pairs:
        newvels = check_collision(i[0],i[1])
        i[0].vel = newvels[0]
        i[1].vel = newvels[1]

def draw(canvas):
    drawArena(canvas)
    for block in block_list:
        block.draw_block(canvas)
    sub_update(10000)
    canvas.draw_text("# of Collisions: "+str(collisions),[50,50],12,"white")

# Create a frame and set up the event handlers
frame = simplegui.create_frame("Block Simulation", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.start()