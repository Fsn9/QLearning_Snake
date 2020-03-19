import numpy as np
import random 
import states
import geometry

#0->ground
#1->snake
#2->food

WALL = -1
GROUND = 0
SNAKE = 1
FOOD = 2

class Environment():
	matrix = []
	snake = []
	food = []
	obstacles = []

	def __init__(self,gridWidth,gridHeight,snakeInitialLength,snake,food,strengthLineOfSight,rangeLineOfSight):
		#save grid dimensions
		self.gridWidth = gridWidth
		self.gridHeight = gridHeight
		#save snake and food objects
		self.snake = snake
		self.food = food

		#flags
		self.collidedWithWall = False
		self.ate = False
		self.collidedWithItself = False

		#save strength and range of the line of sight of the snake
		self.rangeLineOfSight = rangeLineOfSight
		self.strengthLineOfSight = strengthLineOfSight

		#check for snake initial length limits
		self.snakeInitialLength = snakeInitialLength
		if snakeInitialLength > gridWidth:
			print('snake initial length out of bounds! higher than gridWidth')
			exit()
		if snakeInitialLength > gridHeight:
			print('snake initial length out of bounds! higher than gridHeight')
			exit()
		#initialize matrix that describes the environment
		self.matrix = np.zeros((int(self.gridHeight),int(self.gridWidth)),dtype=int)

		#define initial positions
		self.resetPositions(snakeInitialLength)

	def __str__(self):
		meAsString = '\n--Environment--'+'\nMy gridSize:'+str(self.gridWidth)+'x'+str(self.gridHeight)+'\n'+str(self.matrix)
		return meAsString

	def getEntities(self):
		return [WALL,GROUND,SNAKE,FOOD]

	def getSnakeData(self):
		return self.snake.getBody()

	def getMatrix(self):
		return self.matrix

	def getFoodData(self):
		return self.food

	def randomizeDirection(self):
		#choose direction randomly in which the body will grow
		direction = random.uniform(0,1)
		if direction < 0.25:
			return 'left'
		elif direction >= 0.25 and direction < 0.5:
			return 'up'
		elif direction >= 0.5 and direction < 0.75:
			return 'right' 
		else:
			return 'down'

	def randomizeXY(self):
		x = random.randint(0,self.gridWidth-1)
		y = random.randint(0,self.gridHeight-1)
		return x,y

	def verifyValidGrowingDirections(self,direction,headCartesianState,snakeInitialLength):
		xHead = headCartesianState.getPosition().getX()
		yHead = headCartesianState.getPosition().getY()

		if direction == 'up' and yHead >= snakeInitialLength - 1:
			return True
		elif direction == 'left' and xHead >= snakeInitialLength - 1:
			return True
		elif direction == 'down' and self.gridHeight - 1 - yHead >= snakeInitialLength - 1:
			return True
		elif direction == 'right' and self.gridWidth - 1 - xHead >= snakeInitialLength - 1:
			return True
		else:
			return False

	def resetPositions(self,snakeInitialLength):
		self.matrix.fill(0)
		self.snake.resetBody()
		direction = self.randomizeDirection()
		
		for index in range(snakeInitialLength):
			if index == 0:
				#set head of the snake
				xHead,yHead = self.randomizeXY()
				headCartesianState = states.CartesianState(xHead,yHead)
				self.matrix[yHead][xHead] = SNAKE
				self.snake.setHeadPosition(headCartesianState)

				#if direction is not valid, choose another one randomly until it is ok
				if self.verifyValidGrowingDirections(direction,headCartesianState,snakeInitialLength) == False:
					while self.verifyValidGrowingDirections(direction,headCartesianState,snakeInitialLength) == False:
						direction = self.randomizeDirection()
			else:
				lastBodyPart = index - 1
				#set other body parts
				if direction == 'left':
					xBodyPart = self.snake.getBody()[lastBodyPart].getPosition().getX()-1
					bodyCartesianState = states.CartesianState(xBodyPart,yHead)
					self.matrix[yHead][xBodyPart] = SNAKE
					self.snake.addNewBodyPart(bodyCartesianState)

				elif direction == 'up':
					yBodyPart = self.snake.getBody()[lastBodyPart].getPosition().getY()-1
					bodyCartesianState = states.CartesianState(xHead,yBodyPart)
					self.matrix[yBodyPart][xHead] = SNAKE
					self.snake.addNewBodyPart(bodyCartesianState)

				elif direction == 'right':
					xBodyPart = self.snake.getBody()[lastBodyPart].getPosition().getX()+1
					bodyCartesianState = states.CartesianState(xBodyPart,yHead)
					self.matrix[yHead][xBodyPart] = SNAKE
					self.snake.addNewBodyPart(bodyCartesianState)

				else:
					yBodyPart = self.snake.getBody()[lastBodyPart].getPosition().getY()+1
					bodyCartesianState = states.CartesianState(xHead,yBodyPart)
					self.matrix[yBodyPart][xHead] = SNAKE
					self.snake.addNewBodyPart(bodyCartesianState)

				xFood,yFood = self.randomizeXY()
				foodCartesianState = states.CartesianState(xFood,yFood)

				isOverlapped = False

				for eachBodyPart in self.snake.getBody():
					if self.isOverlapped(foodCartesianState,eachBodyPart):
						isOverlapped = True

				if isOverlapped:
					while isOverlapped:
						xFood,yFood = self.randomizeXY()
						foodCartesianState = states.CartesianState(xFood,yFood)
						isOverlapped = False
						for eachBodyPart in self.snake.getBody():
							if self.isOverlapped(foodCartesianState,eachBodyPart):
								isOverlapped = True

							
				foodCartesianState = states.CartesianState(xFood,yFood)
				self.matrix[yFood,xFood] = FOOD							
				#snake.updateBody(self.snake)
				#set food
				#foodCartesianState,xFood,yFood = self.resetFoodPosition()
				self.updateFoodState(foodCartesianState)
				self.updateSnakeState(xHead,yHead,xFood,yFood)

	def isOverlapped(self,state1,state2):
		if state1.getPosition().getX() == state2.getPosition().getX() and state1.getPosition().getY() == state2.getPosition().getY():
			return True
		else:
			return False
	def resetFoodPosition(self):
		whereFood = np.where(self.matrix == FOOD)

		self.matrix[whereFood[0][0],whereFood[1][0]] = 0

		xFood,yFood = self.randomizeXY()
		foodCartesianState = states.CartesianState(xFood,yFood)

		isOverlapped = False

		for eachBodyPart in self.snake.getBody():
			if self.isOverlapped(foodCartesianState,eachBodyPart):
				isOverlapped = True

		if isOverlapped:
			while isOverlapped:
				xFood,yFood = self.randomizeXY()
				foodCartesianState = states.CartesianState(xFood,yFood)
				isOverlapped = False
				for eachBodyPart in self.snake.getBody():
					if self.isOverlapped(foodCartesianState,eachBodyPart):
						isOverlapped = True

		self.updateFoodState(foodCartesianState)

		return foodCartesianState,xFood,yFood	

	def stepInTheEnvironment(self,action):
		self.collidedWithWall = False
		self.ate = False
		self.collidedWithItself = False
		direction = self.getDirectionOfMovementOfSnake()
		newState = self.moveAgent(self.snake.move(action,direction))
		reward = self.computeReward()
		self.updateEnvironment()
		return newState,reward

	def getDirectionOfMovementOfSnake(self):
		NECK_INDEX = 1
		headState = self.snake.getHead()
		neckState = self.snake.getBody()[NECK_INDEX]

		return self.whichSide(headState,neckState)

	def whichSide(self,mainPoint,otherPoint):
		xMain = mainPoint.getX()
		yMain = mainPoint.getY()

		xOther = otherPoint.getX()
		yOther = otherPoint.getY()

		if xMain-xOther < 0:
			return 'left'
		elif xMain-xOther > 0:
			return 'right'
		elif yMain-yOther < 0:
			return 'up'
		elif yMain-yOther > 0:
			return 'down'

	def moveAgent(self,newPosition):
		movement = self.canAgentMove(newPosition)
		if movement == 'OK':
			newState = self.updateSnakeState(self.snake.getX(),self.snake.getY(),self.food.getX(),self.food.getY())

		elif movement == 'wall':
			self.collidedWithWall = True
			self.resetPositions(self.snakeInitialLength)
			newState = self.updateSnakeState(self.snake.getX(),self.snake.getY(),self.food.getX(),self.food.getY())

		elif movement == 'itself':
			self.collidedWithItself = True
			self.resetPositions(self.snakeInitialLength)
			newState = self.updateSnakeState(self.snake.getX(),self.snake.getY(),self.food.getX(),self.food.getY())

		elif movement == 'food':
			self.ate = True
			self.resetFoodPosition()
			self.snake.grow(self.getDirectionOfMovementOfSnake())
			newState = self.updateSnakeState(self.snake.getX(),self.snake.getY(),self.food.getX(),self.food.getY())
		return newState

	def canAgentMove(self,position):
		ok = self.movementInsideBoundaries(position)
		selfCollision = self.selfCollided(position)
		ateFood = self.foodWasEaten(position)
		if ok and not selfCollision and not ateFood:
			return 'OK'
		elif ok and selfCollision:
			return 'itself'
		elif ok and ateFood:
			return 'food'
		elif not ok:
			return 'wall'

	def movementInsideBoundaries(self,position):
		if position.getX() < self.gridWidth and position.getX() >= 0 and position.getY() < self.gridHeight and position.getY() >= 0:
			return True
		else:
			return False

	def updateEnvironment(self):
		xSnake = self.snake.getX()
		ySnake = self.snake.getY()

		xFood = self.food.getX()
		yFood = self.food.getY()

		self.matrix.fill(0)

		for bodyPart in self.snake.getBody():
			self.matrix[bodyPart.getY(),bodyPart.getX()] = SNAKE
		self.matrix[yFood,xFood] = FOOD	


	def updateFoodState(self,newState):
		self.food.setState(newState)

	def updateSnakeState(self,xHead,yHead,xFood,yFood):
		snakeCartesianState = states.CartesianState(xHead,yHead)
		polarStateSnakeRelatedToFood = geometry.generatePolarState(xHead,yHead,xFood,yFood)
		direction_ = self.getDirectionOfMovementOfSnake()

		lineOfSightState = geometry.getLineOfSight(self.gridWidth,self.gridHeight,\
		self.strengthLineOfSight,\
		snakeCartesianState,direction_,self.matrix,self.rangeLineOfSight)

		stateSnake = (polarStateSnakeRelatedToFood,lineOfSightState)
		#print(lineOfSightState)
		self.snake.setState(stateSnake)

		return stateSnake	

	def computeReward(self):
		if self.ate:
			return 100
		elif self.collidedWithWall:
			return -80
		elif self.collidedWithItself:
			return -70
		else:
			return -self.distanceToFood()

	def distanceToFood(self):
		return geometry.distanceBetweenTwoPoints(self.snake.getX(),self.snake.getY(),self.food.getX(),self.food.getY())
	
	def foodWasEaten(self,position):
		return position.getX() == self.food.getX() and position.getY() == self.food.getY()

	def foodEaten(self):
		return self.ate

	def collisionWithWall(self):
		return self.collidedWithWall

	def selfCollided(self,position):
		HEAD_INDEX = 0
		for index,bodyPart in enumerate(self.snake.getBody()):
			if index == HEAD_INDEX:
				continue
			if bodyPart.getX() == position.getX() and bodyPart.getY() == position.getY():
				return True
		return False

	def collisionWithItself(self):
		return self.collidedWithItself
