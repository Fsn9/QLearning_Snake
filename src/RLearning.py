import Environment as env
import entities as ent
import QTable as qt
import random
import actions

SNAKE_INITIAL_LENGTH = 2
EPSILON = 0.95
GAMMA = 0.95
ALPHA = 0.1
MAX_STEPS_PER_EPISODE = 36
EPISODES = 4000

#range and strength of the line of sight
RANGE_LINE_OF_SIGHT = 1
STRENGTH_LINE_OF_SIGHT = 'low'

class RLearning():
	environment = []
	agent = []
	food = []
	obstacles = []
	QTable = []
	def __init__(self,gridWidth,gridHeight,numObstacles):
		# create snake and food objects
		self.agent = ent.Snake(SNAKE_INITIAL_LENGTH)
		self.food = ent.Food()
		#print('PUTA:',self.agent)

		# set the environment
		self.environment = env.Environment(gridWidth,gridHeight,SNAKE_INITIAL_LENGTH,self.agent,self.food,STRENGTH_LINE_OF_SIGHT,RANGE_LINE_OF_SIGHT)

		# set parameters
		self.actualEpsilon = EPSILON
		self.actualGamma = GAMMA
		self.actualAlpha = ALPHA
		self.episodesLeft = EPISODES
		self.numberOfstepsTaken = 0

		# init QTable
		self.QTable = qt.QTable(gridWidth, gridHeight)
		self.QTable.initTable(gridWidth,gridHeight,RANGE_LINE_OF_SIGHT,STRENGTH_LINE_OF_SIGHT,self.environment.getEntities())


	def __str__(self):
		pass

	def getAgent(self):
		return self.agent

	def getEnvironment(self):
		return self.environment

	def learningIsOver(self):
		if self.episodesLeft == 0:
			return True
		else:
			return False

	def updateCountersAndDecayingParameters(self):		
		if self.environment.collisionWithWall() or self.environment.collisionWithItself() or self.numberOfstepsTaken == MAX_STEPS_PER_EPISODE:
			#statistics
			#print('itself:',self.environment.collisionWithItself())
			#print('wall:',self.environment.collisionWithWall())
			#self.arrayAverage.pop()
			#self.arrayAverage.insert(0,self.numberOfstepsTaken)
			#self.average = sum(self.arrayAverage) / len(self.arrayAverage)
			self.numberOfstepsTaken = 0
			self.episodesLeft -= 1
			self.environment.resetPositions(SNAKE_INITIAL_LENGTH)
			print('episodesLeft:',self.episodesLeft)
			self.actualEpsilon = ((self.episodesLeft-EPISODES)/EPISODES)*EPSILON+EPSILON
			self.actualGamma = 0.5*((self.episodesLeft-EPISODES)/EPISODES)*GAMMA+GAMMA


		else:
			#print('STEPS:\n',self.numberOfstepsTaken)
			self.numberOfstepsTaken += 1
			if self.environment.foodEaten():
				self.numberOfstepsTaken-=10

	def decideAction(self):
		randomNumber = random.uniform(0,1)
		#print('MY BODY:',print(self.environment.getSnakeData()))
		if(randomNumber > self.actualEpsilon):
			state = self.agent.getState()
			print('INTELLIGENT')
			#lookup at the table for the best action in the actual state
			bestQ,bestAction = self.QTable.findBestQandAction(state)
			return bestAction,state,bestQ

		else:
			state = self.agent.getState()
			print('RANDOM')
			#random choose an action
			action = self.generateRandomNumber(0,actions.NUM_DIRECTIONS-1)
			Q = self.QTable.findQ(state,action)
			return action,state,Q

	def generateRandomNumber(self,start,end):
		return random.randint(start,end)

	def isFinalState(self,state):
		POLAR_STATE_INDEX = 0
		return (state[POLAR_STATE_INDEX].getRo() == 0 and state[POLAR_STATE_INDEX].getTheta() == 0) or self.environment.collisionWithItself() or self.environment.collisionWithWall()
		

	def act(self):
		#decrement possible steps to take and checks if episode is over
		self.updateCountersAndDecayingParameters()

		#decide Action
		action,oldState,oldQ = self.decideAction()

		#print('oldState',oldState[0].getRo(),oldState[0].getTheta(),oldState[1],'action:',actions.toString(action))

		#do Action
		newState,reward = self.environment.stepInTheEnvironment(action)

		#print('newState',newState[0].getRo(),newState[0].getTheta(),newState[1],'reward',reward)

		if self.isFinalState(newState):
			newQ = oldQ  + self.actualAlpha*(reward - oldQ)
		else:
			maxQ,_ = self.QTable.findBestQandAction(newState)
			newQ = oldQ  + self.actualAlpha*(reward + self.actualGamma * maxQ - oldQ)

		#update QTable		
		self.QTable.setNewQ(oldState,action,newQ)



