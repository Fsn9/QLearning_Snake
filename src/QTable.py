import geometry
import StateAction as sa
import actions
import states


# state = (roFood,thetaFood,[left,front,right]) ~ (food and lineOfSightNeighbourhood)
# action = FORWARD,LEFT,RIGHT

POLAR_STATE_INDEX = 0
LINE_OF_SIGHT_INDEX = 1
LEFT_INDEX = 0
FRONT_INDEX = 1
RIGHT_INDEX = 2

class QTable():
	table = []

	def __init__(self, gridWidth, gridHeight):
			self.numActions = actions.NUM_DIRECTIONS
			self.gridWidth = gridWidth
			self.gridHeight = gridHeight

	def initTable(self, rangeLineOfSight,strengthLineOfSight,entities):
			#Get array of all polar states related to the Food
			allPolarStates = geometry.getAllPolarStatesRelatedToAPoint(self.gridWidth,self.gridHeight)
			allLineOfSightStates = geometry.generateAllStatesLineOfSight(rangeLineOfSight,strengthLineOfSight,entities)
			#Insert elements of the array for each action in an object StateAction in the table
			for polarState in allPolarStates:
				for lineOfSightState in allLineOfSightStates:
					for action in range(actions.NUM_DIRECTIONS):
						self.table.append(sa.StateAction((polarState,[lineOfSightState]),action))
			print('LEN:',len(self.table))

	def display(self):
		for stateAction in self.table:
			print('state:','ro:',stateAction.getState()[POLAR_STATE_INDEX].getRo(),',theta:',stateAction.getState()[POLAR_STATE_INDEX].getTheta(),'lineOfSight:',stateAction.getState()[LINE_OF_SIGHT_INDEX],'\n','action',stateAction.getAction())

	def findQ(self,state,action):
		for stateAction in self.table:
			if self.statesAreEqual(state,stateAction.getState()) and self.actionsAreEqual(action,stateAction.getAction()):
				Q = stateAction.getQ()
				return Q
		return 0

	def setNewQ(self,state,action,newQ):
		for stateAction in self.table:
			if self.statesAreEqual(state,stateAction.getState()) and self.actionsAreEqual(action,stateAction.getAction()):
				stateAction.setQ(newQ)

	def statesAreEqual(self,state1,state2):
		if state1[POLAR_STATE_INDEX].getRo() == state2[POLAR_STATE_INDEX].getRo() \
		and state1[POLAR_STATE_INDEX].getTheta() == state2[POLAR_STATE_INDEX].getTheta() \
		and state1[LINE_OF_SIGHT_INDEX] == state2[LINE_OF_SIGHT_INDEX]:
			return True
		else:
			return False

	def findBestQandAction(self,state):
		bestQ = 0
		bestAction = 0
		maximum = -1000
		for stateAction in self.table:
				if self.statesAreEqual(state,stateAction.getState()):
					if stateAction.getQ() > maximum:
						bestAction = stateAction.getAction()
						bestQ = stateAction.getQ()
						maximum = bestQ
					else:
						continue
				else:
					continue
		return bestQ,bestAction

	def actionsAreEqual(self,action1,action2):
		if action1 == action2:
			return True
		else:
			return False

	def getTable(self):
		return self.table

	def getTableLength(self):
		return len(self.table)






