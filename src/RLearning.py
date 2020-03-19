import Environment as env
import entities as ent
import QTable as qt
import random
import actions

SNAKE_INITIAL_LENGTH = 2
EPSILON = 0.95
GAMMA = 0.95
ALPHA = 0.1
MAX_STEPS_PER_EPISODE = 15
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
		#print(self.agent)

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
		self.QTable.initTable(RANGE_LINE_OF_SIGHT,STRENGTH_LINE_OF_SIGHT,self.environment.getEntities())

		# statistics
		#steps
		self.arrayAverageSteps = [MAX_STEPS_PER_EPISODE]*10
		self.arrayAverageReward = [0]*30
		#reward
		self.averageReward = 0
		self.averageSteps = 0
		self.lastReward = 0
		#collisions
		self.counterCollisionsWithItself = 0
		self.counterCollisionsWithWall = 0
		self.movingAverageArrayWallCollisions = [0]*20
		self.movingAverageWallCollisions = 0
		self.auxiliarCounterCollisions = 0
		self.wallCollisionsSamplingFrequency = 10
		self.auxiliarCounterCollisionsEpisodes = 0




	def __str__(self):
		pass

	def getStatisticalData(self):
		return self.averageReward,self.averageSteps,self.actualEpsilon,self.actualGamma,self.episodesLeft,self.counterCollisionsWithWall,self.counterCollisionsWithItself,self.movingAverageWallCollisions

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
			self.auxiliarCounterCollisionsEpisodes+=1
			self.counterCollisionsWithWall+=1
			self.auxiliarCounterCollisions+=1

			if self.auxiliarCounterCollisionsEpisodes == self.wallCollisionsSamplingFrequency:
				self.movingAverageArrayWallCollisions.pop()
				self.movingAverageArrayWallCollisions.insert(0,self.auxiliarCounterCollisions)
				self.movingAverageWallCollisions = sum(self.movingAverageArrayWallCollisions) / len(self.movingAverageArrayWallCollisions)
				self.auxiliarCounterCollisions = 0
				self.auxiliarCounterCollisionsEpisodes = 0


			if self.environment.collisionWithItself():
				self.counterCollisionsWithItself+=1

			self.arrayAverageSteps.pop()
			self.arrayAverageSteps.insert(0,self.numberOfstepsTaken)
			self.averageSteps = sum(self.arrayAverageSteps) / len(self.arrayAverageSteps)



			self.numberOfstepsTaken = 0
			self.episodesLeft -= 1
			self.environment.resetPositions(SNAKE_INITIAL_LENGTH)
			#print('episodesLeft:',self.episodesLeft)
			self.actualEpsilon = ((self.episodesLeft-EPISODES)/EPISODES)*EPSILON+EPSILON
			self.actualGamma = 0.5*((self.episodesLeft-EPISODES)/EPISODES)*GAMMA+GAMMA


		else:
			#print('STEPS:\n',self.numberOfstepsTaken)
			self.numberOfstepsTaken += 1
			self.arrayAverageReward.pop()
			self.arrayAverageReward.insert(0,self.lastReward)
			self.averageReward = sum(self.arrayAverageReward) / len(self.arrayAverageReward)
			if self.environment.foodEaten():
				self.numberOfstepsTaken = 0

	def decideAction(self):
		randomNumber = random.uniform(0,1)
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

	def isFinalState(self):
		return self.environment.collisionWithItself() or self.environment.collisionWithWall()
		

	def act(self):
		#decrement possible steps to take and checks if episode is over
		self.updateCountersAndDecayingParameters()

		#decide Action
		action,oldState,oldQ = self.decideAction()

		#print('oldState',oldState[0].getRo(),oldState[0].getTheta(),oldState[1],'action:',actions.toString(action))

		#do Action
		newState,reward = self.environment.stepInTheEnvironment(action)

		#print('newState',newState[0].getRo(),newState[0].getTheta(),newState[1],'reward',reward)

		if self.isFinalState():
			newQ = oldQ  + self.actualAlpha*(reward - oldQ)
		else:
			maxQ,_ = self.QTable.findBestQandAction(newState)
			newQ = oldQ  + self.actualAlpha*(reward + self.actualGamma * maxQ - oldQ)

		#update QTable		
		self.QTable.setNewQ(oldState,action,newQ)
		#print('newQ:',newQ,'reward:',reward)
		#statistics
		self.lastReward = reward



