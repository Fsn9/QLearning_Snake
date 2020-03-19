import Position as pos
import states 
import geometry
import random
import actions

class Entity():
	def __init__(self,x,y):
		self.cartesianState = states.CartesianState(x,y)
	def updateCartesianState(self,cartesianState):
		self.cartesianState = cartesianState
	def getCartesianState(self):
		return self.cartesianState
	def getX(self):
		return self.cartesianState.getPosition().getX()
	def getY(self):
		return self.cartesianState.getPosition().getY()


class MovableEntity(Entity):
	#basic
	def goUp(self):
		return pos.Position(self.position.getX(),self.position.getY()-1)
	def goDown(self):
		return pos.Position(self.position.getX(),self.position.getY()+1)
	def goLeft(self):
		return pos.Position(self.position.getX()-1,self.position.getY())
	def goRight(self):
		return pos.Position(self.position.getX()+1,self.position.getY())

class Agent(MovableEntity):
	polarState = []
	def getPolarState(self):
		return self.polarState

	def updateState(self,myNewPosition,myNewPolarState):
		self.polarState = myNewPolarState
		self.position = myNewPosition

	def getState(self):
		return self.polarState,self.position

	def setPolarState(self,polarState):
		self.polarState = polarState

class Snake(MovableEntity):
	def __init__(self,initialLength):
		self.length = initialLength
		self.body = []
		self.state = []
		self.lastTail = []

	def __str__(self):
		return '--SNAKE--\n'+'my body. list of (x,y) from head to tail:'+str([[eachBodyPart.getPosition().getX(),eachBodyPart.getPosition().getY()] for eachBodyPart in self.body])+'\n'

	def getX(self):
		return self.body[0].getX()

	def getY(self):
		return self.body[0].getY()

	def getLength(self):
		return len(self.body)

	def getBody(self):
		return self.body

	def move(self,action,directionSnake):
		if action == actions.FORWARD and directionSnake == 'up':
			self.moveUp()
			return self.getHead()
		elif action == actions.FORWARD and directionSnake == 'down':
			self.moveDown()
			return self.getHead()
		elif action == actions.FORWARD and directionSnake == 'right':
			self.moveRight()
			return self.getHead()
		elif action == actions.FORWARD and directionSnake == 'left':
			self.moveLeft()
			return self.getHead()

		elif action == actions.LEFT and directionSnake == 'up':
			self.moveLeft()
			return self.getHead()
		elif action == actions.LEFT and directionSnake == 'down':
			self.moveRight()
			return self.getHead()
		elif action == actions.LEFT and directionSnake == 'right':
			self.moveUp()
			return self.getHead()
		elif action == actions.LEFT and directionSnake == 'left':
			self.moveDown()
			return self.getHead()

		elif action == actions.RIGHT and directionSnake == 'up':
			self.moveRight()
			return self.getHead()
		elif action == actions.RIGHT and directionSnake == 'down':
			self.moveLeft()
			return self.getHead()
		elif action == actions.RIGHT and directionSnake == 'right':
			self.moveDown()
			return self.getHead()
		elif action == actions.RIGHT and directionSnake == 'left':
			self.moveUp()
			return self.getHead()

	def moveUp(self):
		x = self.getHead().getX()
		y = self.getHead().getY()
		headNewState = states.CartesianState(x,y-1)
		self.lastTail = self.body[-1]
		self.updateBody(headNewState)

	def moveLeft(self):
		x = self.getHead().getX()
		y = self.getHead().getY()
		headNewState = states.CartesianState(x-1,y)
		self.lastTail = self.body[-1]
		self.updateBody(headNewState)	

	def moveRight(self):
		x = self.getHead().getX()
		y = self.getHead().getY()
		headNewState = states.CartesianState(x+1,y)
		self.lastTail = self.body[-1]
		self.updateBody(headNewState)

	def moveDown(self):
		x = self.getHead().getX()
		y = self.getHead().getY()
		headNewState = states.CartesianState(x,y+1)
		self.lastTail = self.body[-1]
		self.updateBody(headNewState)

	def getHead(self):
		return self.body[0]

	def grow(self,direction):
		self.body.append(states.CartesianState(self.lastTail.getX(),self.lastTail.getY()))
		self.lastTail = self.body[-1]

	def updateBody(self,newHeadState):
		for index in range(len(self.body)-1,0,-1):
			self.body[index] = self.body[index-1]
		self.body[0] = newHeadState


	def addNewBodyPart(self,newCartesianState):
		self.body.append(newCartesianState)

	def setHeadPosition(self,newCartesianState):
		self.body.insert(0,newCartesianState)

	def resetBody(self):
		self.body.clear()

	def getState(self):
		return self.state

	def setState(self,state):
		self.state = state

class Food(Entity):
	def __init__(self):
		pass
	def setState(self,state):
		self.cartesianState = state	
	