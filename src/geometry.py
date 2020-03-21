import math
import states
from collections import OrderedDict
import numpy as np
import itertools

PI = 3.1416


opposite = {
	'left' : 'right',
	'right': 'left',
	'down': 'up',
	'up':'down'
}
directions_ = ['up','right','down','left']

def toDegrees(rad):
	return (180/PI)*rad

def toRadians(deg):
	return (PI/180)*deg

def toPolar(x,y):
	ro = math.sqrt(x*x+y*y)
	theta = math.atan2(y,x)
	return ro,theta

def distanceBetweenTwoPoints(x1,y1,x2,y2):
	return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def generatePolarState(agentX,agentY,foodX,foodY):
	ro,theta = toPolar(agentX-foodX,agentY-foodY)
	return states.PolarState(ro,theta)

def generateCartesianState(x,y):
	return states.CartesianState(x,y)

def generatePolarState2(agentX,agentY,foodX,foodY,direction):
	# in a grid where y grows down and x grows right
	# the origin turns to be the snake head and y and x axis pointing in the direction of the movement
	if direction == 'up':
		foodYnew = agentY - foodY
		foodXnew = foodX - agentX
	elif direction == 'left':
		foodYnew = agentX - foodX
		foodXnew = agentY - foodY
	elif direction == 'down':
		foodYnew = foodY - agentY
		foodXnew = agentX - foodX
	elif direction == 'right':
		foodYnew = foodX - agentX
		foodXnew = foodY - agentY
	ro,theta = toPolar2(foodXnew,foodYnew)
	return states.PolarState(ro,theta)

def toPolar2(x,y):
	ro = math.sqrt(x*x+y*y)
	theta = math.atan2(y,x)
		
	return ro,theta


# LINE OF SIGHT #
# high:
# x x x
# x H x
# low:
#   x 
# x H x
def getLineOfSight(envSizeWidth,envSizeHeight,strength,state,direction,environmentMatrixWithoutWalls,range_):
	model = []
	#neighbourhoodStates = []
	thickness = range_
	outInsideConversion = thickness

	wallsModel = getWallsModel(envSizeWidth,envSizeHeight,thickness)
	completeEnvironment = putWalls(environmentMatrixWithoutWalls,wallsModel,thickness)
	if strength == 'low':
		if direction == 'up':
			for range_ in range(1,range_+1):
				head = state
				left = states.CartesianState(state.getX()-range_,state.getY())
				front = states.CartesianState(state.getX(),state.getY()-range_)
				right = states.CartesianState(state.getX()+range_,state.getY())
				#neighbourhoodStates.extend([left,front,right])
				model.append(completeEnvironment[left.getY()+outInsideConversion,left.getX()+outInsideConversion])
				model.append(completeEnvironment[front.getY()+outInsideConversion,front.getX()+outInsideConversion])
				model.append(completeEnvironment[right.getY()+outInsideConversion,right.getX()+outInsideConversion])
		elif direction == 'right':
			head = state
			for range_ in range(1,range_+1):
				left = states.CartesianState(state.getX(),state.getY()-range_)
				front = states.CartesianState(state.getX()+range_,state.getY())
				right = states.CartesianState(state.getX(),state.getY()+range_)
				#neighbourhoodStates.extend([left,front,right])
				model.append(completeEnvironment[left.getY()+outInsideConversion,left.getX()+outInsideConversion])
				model.append(completeEnvironment[front.getY()+outInsideConversion,front.getX()+outInsideConversion])
				model.append(completeEnvironment[right.getY()+outInsideConversion,right.getX()+outInsideConversion])
		elif direction == 'down':
			head = state
			for range_ in range(1,range_+1):
				left = states.CartesianState(state.getX()+range_,state.getY())
				front = states.CartesianState(state.getX(),state.getY()+range_)
				right = states.CartesianState(state.getX()-range_,state.getY())
				#neighbourhoodStates.extend([left,front,right])
				model.append(completeEnvironment[left.getY()+outInsideConversion,left.getX()+outInsideConversion])
				model.append(completeEnvironment[front.getY()+outInsideConversion,front.getX()+outInsideConversion])
				model.append(completeEnvironment[right.getY()+outInsideConversion,right.getX()+outInsideConversion])
		elif direction == 'left':
			head = state
			for range_ in range(1,range_+1):
				left = states.CartesianState(state.getX(),state.getY()+range_)
				front = states.CartesianState(state.getX()-range_,state.getY())
				right = states.CartesianState(state.getX(),state.getY()-range_)
				#neighbourhoodStates.extend([left,front,right])
				model.append(completeEnvironment[left.getY()+outInsideConversion,left.getX()+outInsideConversion])
				model.append(completeEnvironment[front.getY()+outInsideConversion,front.getX()+outInsideConversion])
				model.append(completeEnvironment[right.getY()+outInsideConversion,right.getX()+outInsideConversion])

	elif strength == 'high':
		return None
	return model

def generateAllStatesLineOfSight(rangeLineOfSight,strengthLineOfSight,entities):
	counter = 0
	MAX_SEEN_LOW = 3 * rangeLineOfSight
	MAX_SEEN_HIGH = rangeLineOfSight*(2*rangeLineOfSight+3)
	if strengthLineOfSight == 'low':
		allStates = list(itertools.product(entities,repeat=MAX_SEEN_LOW))
	elif strengthLineOfSight == 'high':
		allStates = list(itertools.product(entities,repeat=MAX_SEEN_HIGH))

	allStates = thereIsOnlyOneFoodSoClean(allStates)

	# convert tuples to list
	allStatesNew = [list(state) for state in allStates]

	return allStatesNew

def thereIsOnlyOneFoodSoClean(lineOfSightPossibilities):
	FOOD = 2
	counterFood = 0
	cleanedList = []
	for eachLineOfSightPossibility in lineOfSightPossibilities:
		counterFood = 0
		for entity in eachLineOfSightPossibility:
			if entity == FOOD:
				counterFood += 1
		if counterFood <= 1:
			cleanedList.append(eachLineOfSightPossibility)
	return cleanedList

def putWalls(envWithoutWalls,envWithWalls,thickness):
	complete = []
	rowsWithout = envWithoutWalls.shape[0]
	colsWithout = envWithoutWalls.shape[1]

	rowsWith = envWithWalls.shape[0]
	colsWith = envWithWalls.shape[1]
	
	envWithWalls[thickness:rowsWithout + thickness,thickness:colsWithout + thickness] = envWithoutWalls[:][:]
	
	return envWithWalls

def getWallsModel(envSizeWidth,envSizeHeight,thickness):
	#create matrix with surrounding walls (-1) and inside environment (0)
	matrixEnvironmentWithWalls = -1*np.ones((envSizeHeight+2*thickness,envSizeWidth+2*thickness),dtype=int)
	matrixEnvironmentWithWalls[thickness:-thickness,thickness:-thickness] = 0
	#get dimensions to use in the loop
	rows = matrixEnvironmentWithWalls.shape[0] 
	cols = matrixEnvironmentWithWalls.shape[1]
	
	return matrixEnvironmentWithWalls


def getCartesianStates(envSizeWidth,envSizeHeight):
	cartesianStates = []
	for col in range(envSizeWidth):
		for row in range(envSizeHeight):
			element = states.CartesianState(col,row)
			cartesianStates.append(element)

	return cartesianStates

def getAllCartesianStatesRelatedToAPoint(envSizeWidth,envSizeHeight):
	foodPossibleStatesArray = getCartesianStates(envSizeWidth,envSizeHeight)
	colFood = 0
	rowFood = 0
	col = 0 
	row = 0
	allCartesianStates = []

	for state in foodPossibleStatesArray:
		colFood = state.getX()
		rowFood = state.getY()
		for col in range(envSizeWidth):
			for row in range(envSizeHeight):
				if col == colFood and row == rowFood:
					continue
				allCartesianStates.append(generateCartesianState(col,row))
				row+=1

			col+=1

	return allCartesianStates	

def getAllPolarStatesRelatedToAPoint(envSizeWidth,envSizeHeight):
	foodPossibleStatesArray = getCartesianStates(envSizeWidth,envSizeHeight)
	colFood = 0
	rowFood = 0
	col = 0 
	row = 0
	allPolarStates = []

	#array that will contain all pairs including duplicate states
	allRoThetaPairsUnfilteredList = []

	#array that will contain all pairs excluding duplicate states
	allRoThetaPairsFiltereredList = []

	for state in foodPossibleStatesArray:
		colFood = state.getX()
		rowFood = state.getY()
		for col in range(envSizeWidth):
			for row in range(envSizeHeight):
				if col == colFood and row == rowFood: # is this correct? not counting with the state in which they are overlapped
					continue
				state = generatePolarState(col,row,colFood,rowFood)
				allRoThetaPairsUnfilteredList.append((state.getRo(),state.getTheta()))

	allRoThetaPairsFiltereredList = list(dict.fromkeys(allRoThetaPairsUnfilteredList))

	for pairRoTheta in allRoThetaPairsFiltereredList:
		allPolarStates.append(states.PolarState(pairRoTheta[0],pairRoTheta[1]))

	return allPolarStates

def getAllPolarStatesRelatedToAPoint2(envSizeWidth,envSizeHeight):
	foodPossibleStatesArray = getCartesianStates(envSizeWidth,envSizeHeight)
	colFood = 0
	rowFood = 0
	col = 0 
	row = 0
	allPolarStates = []

	#array that will contain all pairs including duplicate states
	allRoThetaPairsUnfilteredList = []

	#array that will contain all pairs excluding duplicate states
	allRoThetaPairsFiltereredList = []
	for direction in directions_:
		for state in foodPossibleStatesArray:
			colFood = state.getX()
			rowFood = state.getY()
			for col in range(envSizeWidth):
				for row in range(envSizeHeight):
					if col == colFood and row == rowFood: # is this correct? not counting with the state in which they are overlapped
						continue
					state = generatePolarState2(col,row,colFood,rowFood,direction)
					allRoThetaPairsUnfilteredList.append((state.getRo(),state.getTheta()))

	allRoThetaPairsFiltereredList = list(dict.fromkeys(allRoThetaPairsUnfilteredList))	

	for pairRoTheta in allRoThetaPairsFiltereredList:
		allPolarStates.append(states.PolarState(pairRoTheta[0],pairRoTheta[1]))

	return allPolarStates
