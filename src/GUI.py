import tkinter as tk


class GUI(tk.Tk):

    def __init__(self, rl, width, height, gridWidth, gridHeight, pixelSize):
        # initialize a Tk object
        tk.Tk.__init__(self)

        # save reinforcement learning object
        self.rl = rl

        # define objects containing rectangles of food and snake
        self.snakeGUI = []
        self.foodGUI = []

        # save dimensions as attributes
        self.width = width
        self.height = height
        self.pixelSize = pixelSize
        self.gridWidth = gridWidth
        self.gridHeight = gridHeight

        # set geometry
        self.geometry(str(self.width) + "x" + str(self.height))

        # draw canvas
        self.canvas = self.setCanvas(self.width, self.height, "black")
        self.canvas.grid(row=0, column=0, columnspan=2, sticky=tk.W + tk.E + tk.N + tk.S)

        # draw labels
        self.labelReward = self.createLabel('Average reward:',1,0)
        self.labelRewardval = self.createLabel(str(self.rl.averageReward),1,1)
        self.labelSteps = self.createLabel('Average steps:',2,0)
        self.labelStepsval = self.createLabel(str(self.rl.averageSteps),2,1)
        self.labelEpsilon = self.createLabel('Epsilon:',3,0)
        self.labelEpsilonval = self.createLabel(str(self.rl.actualEpsilon),3,1)
        self.labelGamma = self.createLabel('Gamma:',4,0)
        self.labelGammaval = self.createLabel(str(self.rl.actualGamma),4,1)
        self.labelEpisodesLeft = self.createLabel('EpisodesLeft:',5,0)
        self.labelEpisodesLeftval = self.createLabel(str(self.rl.actualGamma),5,1)
        self.labelCollisionsWall = self.createLabel('Wall collisions:',6,0)
        self.labelCollisionsWallval = self.createLabel(str(self.rl.counterCollisionsWithWall),6,1)
        self.labelCollisionsItself = self.createLabel('Self collisions:',7,0)
        self.labelCollisionsItselfval = self.createLabel(str(self.rl.counterCollisionsWithItself),7,1)

        # draw walls
        self.drawWalls()

        # start learning process
        self.startLearning()



    def __str__(self):
        return '--GUI--' + '\n' + 'width = ' + str(self.width) + ' pixels' + '\nheight = ' + str(
            self.height) + ' pixels' + '\npixelSize = ' + str(int(self.pixelSize)) + ' pixels'

    def createLabel(self,text,row,col):
        label = tk.Label(text = text)
        label.grid(row=row,column=col)
        return label   

    def setCanvas(self, width, height, color):
        canvas = tk.Canvas(width = width, height = height, bg = color)
        return canvas

    def drawRectangle(self, x, y, color):
        rectangle = self.canvas.create_rectangle(x * self.pixelSize, y * self.pixelSize, (1 + x) * self.pixelSize,
                                            (1 + y) * self.pixelSize, fill=color)
        return rectangle

    def drawWalls(self):
        for x in range(self.gridWidth):
            self.drawRectangle(x,0,'green')
        for y in range(1,self.gridHeight):
            self.drawRectangle(0,y,'green')
        for y in range(1,self.gridHeight):
            self.drawRectangle(self.gridWidth-1,y,'green')
        for x in range(1,self.gridWidth):
            self.drawRectangle(x,self.gridHeight-1,'green')

    def draw(self):
        snakeBody = self.rl.getEnvironment().getSnakeData()

        for index,eachBodyPart in enumerate(snakeBody):
            if index == 0:
                self.snakeGUI.append(self.drawRectangle(eachBodyPart.getX()+1, eachBodyPart.getY()+1, 'white'))
            else:
                self.snakeGUI.append(self.drawRectangle(eachBodyPart.getX()+1, eachBodyPart.getY()+1, 'orange'))

        food = self.rl.getEnvironment().getFoodData()
        self.foodGUI = self.drawRectangle(food.getX()+1, food.getY()+1, 'red')
        
        reward,steps,epsilon,gamma,episodes,wallCollisions,selfCollisions = self.rl.getStatisticalData()
        self.labelStepsval.config(text=str(steps)[0:6])
        self.labelGammaval.config(text=str(gamma)[0:6])
        self.labelEpsilonval.config(text=str(epsilon)[0:6])
        self.labelRewardval.config(text=str(reward)[0:6])
        self.labelEpisodesLeftval.config(text=str(episodes)[0:6])
        self.labelCollisionsItselfval.config(text=str(selfCollisions)[0:6])
        self.labelCollisionsWallval.config(text=str(wallCollisions)[0:6])

    def clear(self):
        for bodyPart in self.snakeGUI:
            self.canvas.delete(bodyPart)
        self.canvas.delete(self.foodGUI)

    def repaint(self):
        self.clear()
        self.draw()

    def startLearning(self):
        self.runRL()

    def runRL(self):
        if self.rl.learningIsOver():
            return
        else:
            self.repaint()
            self.rl.act()

        self.after(1,self.startLearning)
    
        
