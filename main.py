'''
2D PSO.
Draft 1 - psoDraft1.py
Recorded in research journal under 6/2/2016
Algorithm and Research Referenced from Quek Jie Ren Jeremy "A study on PSO"

Created 6 Feb - 9 Feb 2016 (#772 - 775)
Updated 3 June 2016 

'''
import time;
import random;
import math;
try:
    import tkinter as tk;
except:
    import Tkinter as tk;

'''
1. Defining the function in question.
'''

#for particle chase mouse function
def motion(e):
    global mouseX, mouseY
    mouseX, mouseY = (((e.x-100)*(2*LIMX)/1200)-LIMX), (((e.y-50)*(2*LIMY)/600)-LIMY)

def function(a, b, n):
    #return -(1 + math.cos(12*((a**2+b**2)**0.5)))/((0.5*(a**2+b**2)) + 2) + 1
    #return ((a**2)+(b**2))**0.5
    return ((a-mouseX)**2 + (b-mouseY)**2)**0.5
'''
2. The main particle object.
'''
        
class particles():

    #2A(1): Draws particles on canvas.  Called each time particles are updated.

    def drawParticles(self, canvas):
        
        for i in range(self.n):
            stepX = 1200/(self.limX*2)
            stepY = 600/(self.limY*2)
            x = int((self.px[i]+self.limX)*stepX+100)
            y = int((self.py[i]+self.limY)*stepY+50)
            
            canvas.delete(self.markers[i])
            self.markers[i] = canvas.create_oval(x-4, y-4, x+5, y+5, fill="", outline="black")
            
        canvas.focus_set()

    #2A(2): Creates the particle id on canvas.  Called once the tkinter GUI is opened.
        
    def drawParticlesINIT(self):
        
        for i in range(self.n):
            stepX = 1200/(self.limX*2)
            stepY = 600/(self.limY*2)
            x = int((self.px[i]+self.limX)*stepX+100)
            y = int((self.py[i]+self.limY)*stepY+50)
            
            self.markers.append(self.canvas.create_oval(x-4, y-4, x+5, y+5, fill = "", outline="black"))
            
        canvas.focus_set()      

    #2B: Initialisation function.
    def __init__(self, n, limX, limY, weight, cSoc, cCog, canvas):

        #object parameters
        self.n = n;
        self.isMoving = 0;
        self.canvas = canvas
        self.cSoc = []
        self.cCog = []
        self.w = []

        self.limX = limX 
        self.limY = limY
        
        self.functionN = 1;
        self.iteration = 0;

        #object dynamic values
        
        self.vx = []#velocity
        self.vy = []
        self.px = []#position
        self.py = []

        self.markers = []         
        
        self.gbest = 10000000
        self.gbestXPos = 5
        self.gbestYPos = 5
        self.pbestXPos = []
        self.pbestYPos = []
        self.pbest = []

        #other object attributes / statistics

        self.constancy = 0;
        self.prevBest = 0;

        self.distance = []
        self.distanceMarker = []
        
        for i in range(n):
            #initialise the velocities - consider using other methods - play around!
            self.vx.append(random.random()*10-5);
            self.vy.append(random.random()*10-5);
            
            self.pbest.append(10000000);
            self.pbestXPos.append(5);
            self.pbestYPos.append(5);
            self.w.append(weight);
            self.cSoc.append(cSoc);
            self.cCog.append(cCog);
            self.distance.append(0);
            self.distanceMarker.append(0);

        for i in range(n):
            self.px.append(random.random()*2*limX - limX)
            self.py.append(random.random()*2*limY - limY)

        self.drawParticlesINIT()
        
        
            
    def update(self):
        vx = self.vx
        vy = self.vy
        cSoc = self.cSoc
        cCog = self.cCog
        px = self.px
        py = self.py
        w = self.w
        gbest = self.gbest
        pbest = self.pbest
        gbestXPos = self.gbestXPos
        gbestYPos = self.gbestYPos
        pbestXPos = self.pbestXPos
        pbestYPos = self.pbestYPos
        distance = self.distance

        self.gbest = function(self.gbestXPos, self.gbestYPos, 0) #dynamic function
        
        maxDistance = 0
        self.iteration += 1
        
        for i in range(self.n):
            r1 = random.random()
            r2 = random.random()          
            
            position = function(px[i], py[i], self.functionN)

            #use self. when updating, variable name alone when retrieving values.
            #update the best positions.
            if(position < gbest):
                self.gbestXPos = px[i]
                self.gbestYPos = py[i]
                self.gbest = position
            if(position < pbest[i]):
                self.pbest[i] = position
                self.pbestXPos[i] = px[i]
                self.pbestYPos[i] = py[i]
            
            vx[i] = w[i]*vx[i] + cSoc[i]*r1*(gbestXPos - px[i]) + cCog[i]*r2*(pbestXPos[i] - px[i])
            vy[i] = w[i]*vy[i] + cSoc[i]*r1*(gbestYPos - py[i]) + cCog[i]*r2*(pbestYPos[i] - py[i])
                    
            tx = (px[i] + vx[i])
            ty = (py[i] + vy[i])
            distance[i] += (vx[i]**2+vy[i]**2)**(0.5)
            if(distance[i] > maxDistance):
                maxDistance = distance[i]
            graphY = int(GRAPH_HEIGHT - (distance[i]/maxDistance) * GRAPH_HEIGHT)
            graphX = int((i/self.n)*GRAPH_WIDTH)+6
            graphCanvas.delete(self.distanceMarker[i])
            self.distanceMarker[i] = graphCanvas.create_rectangle(graphX, graphY, graphX+1, GRAPH_HEIGHT-2, outline="red")
            
            
            if(tx > 0):                
                px[i] = min(tx, self.limX)
            else:
                px[i] = max(tx, -self.limX)
                
            if(ty > 0):                
                py[i] = min(ty, self.limY)
            else:
                py[i] = max(ty, -self.limY)
            #print(gbest)
            #print(px[i], py[i])
                
        self.drawParticles(self.canvas)

    def printResults(self):
        #find the modal position
        #or just output gbest!
        global PARAMETERS

        foo = str(round(self.gbest, ROUNDING))
        bar = str(round(self.gbestXPos, ROUNDING))
        baz = str(round(self.gbestYPos, ROUNDING))
        if bar == "-0.0":
            bar = "0.0"
        if baz == "-0.0":
            baz = "0.0"
        
        print(foo, " is found at ", bar, ",", baz)

        self.canvas.itemconfig(LABELS[4], text = str(self.iteration))
        self.canvas.itemconfig(LABELS[5], text = str(foo))
        self.canvas.itemconfig(LABELS[6], text = str(bar))
        self.canvas.itemconfig(LABELS[7], text = str(baz))
        self.canvas.itemconfig(LABELS[8], text = str(mouseX))
        self.canvas.itemconfig(LABELS[9], text = str(mouseY))
        self.canvas.itemconfig(LABELS[10], text = "Swarming...")

        #self.canvas.itemconfig(LABELS[0], text="asdf")
        return round(self.gbest, ROUNDING)

    def finalResults(self, mode):
        #after auto-stop
        self.canvas.itemconfig(LABELS[10], text = "Stopped")
        if(mode == -1):
            print("Function has stopped automatically!")
        if(mode == 0):
            print("Function stopped by user!")
        print("===================================")
        print("Gloabl Best: ", round(self.gbest, ROUNDING))
        print("XPOS of Best:", round(self.gbestXPos, ROUNDING))
        print("YPOS of Best:", round(self.gbestYPos, ROUNDING))
        print("===================================")
        print("")
        print("")
        print("")
    
    def iterate(self):
        if self.isMoving == 1:
            x = self.printResults()
            if(self.prevBest == x):
                self.constancy += 1
            self.prevBest = x
            if(self.constancy > LIMIT):
                self.isMoving = -1
            self.update()
            root.after(DELAY, self.iterate)
        else:
            if self.isMoving == -1:
                self.finalResults(-1)
            else:
                self.finalResults(0)

    def start(self, e):
        self.isMoving = 1
        self.iterate()
        
    def stop(self, e):
        self.isMoving = 0
        self.printResults()
        
'''
3. GUI Elements, Initialisation
'''

#3.1 Distance graph
#done first, so focus will not interfere with main window.
graph = tk.Tk()
graph.title("Distance")
graph.geometry('+2000+100')
graph.resizable(False, False)
graphCanvas = tk.Canvas(graph, width=200, height = 200)
graphCanvas.create_rectangle(3, 0, 5, 200, fill="black")
graphCanvas.create_rectangle(3, 198, 200, 200, fill="black")
graphCanvas.pack()

#3.2 Root Window
root = tk.Tk()
root.title("PSO")
root.geometry('+10+10')

root.resizable(False,False)

#3.3 Canvas object with grid
canvas = tk.Canvas(root, width = 1500, height = 700)
canvas.create_rectangle(100, 348, 1300, 352, fill = "black")
canvas.create_rectangle(698, 50, 702, 650, fill = "black")

canvas.create_rectangle(99, 50, 100, 650, fill = "green")
canvas.create_rectangle(1299, 50, 1300, 650, fill = "green")

canvas.create_rectangle(100, 49, 1300, 50, fill = "green")
canvas.create_rectangle(100, 649, 1300, 650, fill = "green")

INF = 9223372036854775000

#3.4 functional constants
DELAY = 100;
ROUNDING = 4;
LIMIT = 50;
GRAPH_HEIGHT = 200
GRAPH_WIDTH = 200

#3.5 particle spread parameters
N = 50
LIMX = 5
LIMY = 5
WEIGHT = 0.05
CSOC = 4.0
CCOG = 1.5

#3.6 other globals
mouseX = 0
mouseY = 0
paraLabel_one = ["N      = ", "Weight = ", "csoc   = ", "ccog   = "]
paraLabel_two = ["iter # = ", "gbest  = ", "gbestX = ", "gbestY = ", "mouseX = ", "mouseY = "]
PARAMETERS = [str(N), str(WEIGHT), str(CSOC), str(CCOG), str(0), str(INF), str(5), str(5), mouseX, mouseY, ""]

#3.7 Print label on GUI
canvas.create_rectangle(1310, 90, 1490, 610, fill="#0F0F0F")

canvas.create_rectangle(1310, 50, 1490, 90, fill="#1A1A1A")
canvas.create_rectangle(1310, 50, 1490, 52, fill="#01A05A", outline = "#01A05A")
canvas.create_text(1320, 60, text="Swarm Parameters:", anchor = "nw", fill="#BEBEBE", font=("Source Sans Pro", 14))

canvas.create_rectangle(1310, 240, 1490, 280, fill="#1A1A1A")
canvas.create_rectangle(1310, 240, 1490, 242, fill="#3E90BD", outline = "#3E90BD")
canvas.create_text(1320, 250, text="Swarm Results:", anchor = "nw", fill="#BEBEBE", font=("Source Sans Pro", 14))

LABELS = []
for i in range(4):
    canvas.create_text(1320, i*35+100, text=paraLabel_one[i], anchor = "nw", fill = "#FFFFFF", font=("Consolas",14))
    canvas.create_text(1320, (i+4)*35+150, text=paraLabel_two[i], anchor = "nw", fill = "#FFFFFF", font=("Consolas",14))
    LABELS.append(canvas.create_text(1420, i*35+100, text=PARAMETERS[i], anchor = "nw", fill = "#FFFFFF", font=("Consolas",14)))
canvas.create_text(1320, (4+4)*35+150, text=paraLabel_two[4], anchor = "nw", fill = "#FFFFFF", font=("Consolas",14))
canvas.create_text(1320, (5+4)*35+150, text=paraLabel_two[5], anchor = "nw", fill = "#FFFFFF", font=("Consolas",14))

for i in range(6):
    LABELS.append(canvas.create_text(1420, (i+4)*35+150, text=PARAMETERS[i+4], anchor = "nw", fill = "#FFFFFF", font=("Consolas",14)))
LABELS.append(canvas.create_text(1320, (10)*35+150, text=PARAMETERS[8], anchor = "nw", fill = "#FF6607", font=("Consolas",14)))    

canvas.pack()

#3.8 Create Particle Object, key bindings
myParticles = particles(N, LIMX, LIMY, WEIGHT, CSOC, CCOG, canvas)
root.bind('<space>', myParticles.start)
root.bind('<Button-1>', myParticles.stop)
root.bind('<Motion>', motion)

root.focus_set()
root.mainloop();


        
