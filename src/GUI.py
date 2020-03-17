import tkinter as tk


class GUI(tk.Tk):
    snakeGUI = []
    foodGUI = []

    def __init__(self, rl, width, height, gridWidth, gridHeight, pixelSize):
        # initialize a Tk object
        tk.Tk.__init__(self)

        # save reinforcement learning object
        self.rl = rl

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
        self.canvas.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S)

        self.drawWalls()
        self.startLearning()

    def __str__(self):
        return '--GUI--' + '\n' + 'width = ' + str(self.width) + ' pixels' + '\nheight = ' + str(
            self.height) + ' pixels' + '\npixelSize = ' + str(int(self.pixelSize)) + ' pixels'

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

        self.after(2,self.startLearning)
    
        
