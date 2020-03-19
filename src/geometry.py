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
	if x==0 and y>0:
		theta = PI*0.5
	elif x==0 and y<0:
		theta = PI*0.5-PI
	elif y==0 and x>0:
		theta = 0
	elif y==0 and x<0:
		theta = -PI
	elif x==0 and y==0:
		theta = 0.0
	else:
		theta = math.atan2(y,x)
	return ro,theta

def distanceBetweenTwoPoints(x1,y1,x2,y2):
	return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def distanceBetweenTwoCoordinates(x1,x2):
	return x1-x2

def generatePolarState(agentX,agentY,foodX,foodY):
	ro,theta = toPolar(agentX-foodX,agentY-foodY)
	return states.PolarState(ro,theta)

def generateCartesianState(x,y):
	return states.CartesianState(x,y)

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
	#print('\nMODEL:',model)
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
	return allStates

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

# WALLS
def getWallsModel(envSizeWidth,envSizeHeight,thickness):
	#create matrix with surrounding walls (-1) and inside environment (0)
	matrixEnvironmentWithWalls = -1*np.ones((envSizeHeight+2*thickness,envSizeWidth+2*thickness),dtype=int)
	matrixEnvironmentWithWalls[thickness:-thickness,thickness:-thickness] = 0
	#get dimensions to use in the loop
	rows = matrixEnvironmentWithWalls.shape[0] 
	cols = matrixEnvironmentWithWalls.shape[1]
	
	
	'''
	#define an empty dictionary to collect the states of the walls and the side associated
	sideToWalls = {}
	wallsUp = []
	wallsLeft = []
	wallsRight = []
	wallsDown = []

	for eachRow in range(0,rows):
		for eachCol in range(0,cols):
			if matrixEnvironmentWithWalls[eachRow,eachCol] == -1:
				if eachRow == 0:
					wallsUp.append(states.CartesianState(eachCol-1,eachRow-1))
					sideToWalls['up'] = wallsUp
				elif eachRow == envSizeHeight + 1:
					wallsDown.append(states.CartesianState(eachCol-1,eachRow-1))
					sideToWalls['down'] = wallsDown
				elif eachCol == 0 and eachRow != envSizeHeight + 1:
					wallsLeft.append(states.CartesianState(eachCol-1,eachRow-1))
					sideToWalls['left'] = wallsLeft
				else:
					wallsRight.append(states.CartesianState(eachCol-1,eachRow-1))
					sideToWalls['right'] = wallsRight
	'''
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
	#for index,eachState in enumerate(allCartesianStates):
	#	print(index,' X:',eachState.getX(),' Y:',eachState.getY())

	return allCartesianStates	

def getAllPolarStatesRelatedToAPoint(envSizeWidth,envSizeHeight):
	foodPossibleStatesArray = getCartesianStates(envSizeWidth,envSizeHeight)
	colFood = 0
	rowFood = 0
	col = 0 
	row = 0
	allPolarStates = []

	#filter to remove repeated states
	dictionaryFilter = {}

	for state in foodPossibleStatesArray:
		colFood = state.getX()
		rowFood = state.getY()
		for col in range(envSizeWidth):
			for row in range(envSizeHeight):
				if col == colFood and row == rowFood: # is this correct? not counting with the state in which they are overlapped
					continue
				state = generatePolarState(col,row,colFood,rowFood)
				dictionaryFilter[state.getTheta()]=state.getRo()

	#append the values filtered by the dictionary to the list		
	for theta,ro in dictionaryFilter.items():
		allPolarStates.append(states.PolarState(ro,theta))

	#for index,eachState in enumerate(allPolarStates):
	#	print(index,' ro:',eachState.getRo(),' theta:',eachState.getTheta())

	return allPolarStates
'''
def getAllPolarStatesRelatedToNPoints(envSizeWidth,envSizeHeight,nPoints):
	foodPossibleStatesArray = getCartesianStates(envSizeWidth,envSizeHeight)
	colFood = 0
	rowFood = 0
	col = 0 
	row = 0
	allPolarStates = []

	#filter to remove repeated states
	dictionaryFilter = {}

	for state in foodPossibleStatesArray:
		colFood = state.getX()
		rowFood = state.getY()
		for col in range(envSizeWidth):
			for row in range(envSizeHeight):
				if col == colFood and row == rowFood: # is this correct? not counting with the state in which they are overlapped
					continue
				state = generatePolarState(col,row,colFood,rowFood)
				dictionaryFilter[state.getTheta()]=state.getRo()

	#append the values filtered by the dictionary to the list		
	for theta,ro in dictionaryFilter.items():
		allPolarStates.append(states.PolarState(ro,theta))

def getNearestWallsBySide(envSizeWidth,envSizeHeight,state,wallsModel):
	nearestWallBySide = {} 
	nearestWallState = []

	#find nearest walls and save them in a new dict
	for side,values in wallsModel.items():
		minimum = 1000
		for state_ in values:
			m = manhattan(state,state_)
			if m < minimum:
				nearestWallState = state_
				minimum = m
		nearestWallBySide[side] = nearestWallState

	return nearestWallBySide

# envSizeWidth,envSizeEight -> dimensions of the environment
# state -> state in which the agent is in
# direction -> direction in which the agent is pointing to (important to line of sight)
# nWalls -> n walls to be covered in the line of sight
def getNearestWalls(envSizeWidth,envSizeHeight,state,direction,nWalls):
	wallsModel,matrixRepresentation = getWallsModel(envSizeWidth,envSizeHeight)
	nearestWalls = getNearestWallsBySide(envSizeWidth,envSizeHeight,state,wallsModel)
	#displayLineOfSight(state,nearestWalls,matrixRepresentation)

	wallsToDistance = {}
	TURN_AROUND = 2

	#create dictionary that relates each wall to the distance to it
	for side,state_ in nearestWalls.items():
		if side == opposite[direction]:
			wallsToDistance[state_] = manhattan(state_,state) + TURN_AROUND
		else:
			wallsToDistance[state_] = manhattan(state_,state)

	#order walls by distance to facilitate minimum (object returned is a list of tuples)
	wallsToDistanceSorted = sorted(wallsToDistance.items(), key = lambda v: v[1])

	walls = []
	minimum = 10000
	counterWalls = 0

	for element in wallsToDistanceSorted:
		if counterWalls == nWalls:
			break
		if element[1] <= minimum: 		# index 1-> distance
			walls.append(element[0])	# index 0-> wall
			minimum = element[1]
			counterWalls+=1
	print('\n')
	displayLineOfSight2(state,walls,matrixRepresentation)
	#vectors
	wallVector = []
	for w in walls:
		wallVector.append((w.getX(),w.getY()))

	print(wallVector)
	print('sum v:',(sum([pair[0] for pair in wallVector]),sum([pair[1] for pair in wallVector])))



	return walls

def getAllCartesianStatesRelatedToWalls(envSizeWidth,envSizeHeight,nWalls):
	wallsModel,matrixRepresentation = getWallsModel(envSizeWidth,envSizeHeight)
	
	cartesianStates = getCartesianStates(envSizeWidth,envSizeHeight)
	allStates = []
	for state in cartesianStates:
		print('\n')
		for direction in directions_:
			walls = getNearestWalls(envSizeWidth,envSizeHeight,state,direction,nWalls)
			allStates.append(walls)
			matrixRepresentationCopy = matrixRepresentation.copy()
			#print(direction)
			#displayLineOfSight(state,walls,matrixRepresentationCopy)
	return allStates

def displayLineOfSight(state,nearestWalls,wallModel):
	for k,v in nearestWalls.items():
		x = v.getX()
		y = v.getY()
		wallModel[y+1][x+1] = 8
	wallModel[state.getY()+1][state.getX()+1] = 9
	print(wallModel)

def displayLineOfSight2(state,nearestWalls,wallModel):
	# 8->nearestWalls
	# 9->agent
	# 0->blank
	# -1->wall

	for wall in nearestWalls:
		x = wall.getX()
		y = wall.getY()
		wallModel[y+1][x+1] = 8
	wallModel[state.getY()+1][state.getX()+1] = 9
	print(wallModel)	

def manhattan(state1,state2):
	return abs(state1.getX()-state2.getX())+ abs(state1.getY()-state2.getY())



def test():
	w = 10
	h = 10
	direction = 'right'
	strengthLineOfSight = 'low'
	x = 1
	y = 0
	state_ = states.CartesianState(x,y)
	env = np.zeros((h,w),dtype=int)
	env[y,x]=1
	env[y,x+1]=1
	
	#print('cartesianStates:')
	#allCartesianStates = getCartesianStates(w,h)
	#print(len(allCartesianStates))
	#print([[eachCartesianState.getX(),eachCartesianState.getY()] for eachCartesianState in getCartesianStates(w,h)])
	#print('\n\n')
	#print('cartesianStatesRelated:')
	#allCartesianStatesRelated = getAllCartesianStatesRelatedToAPoint(w,h)
	#print(len(allCartesianStatesRelated))
	#print([[eachCartesianState.getX(),eachCartesianState.getY()] for eachCartesianState in getAllCartesianStatesRelatedToAPoint(w,h)])
	print('\n\n')
	print('polarStatesRelated:')
	allPolarStates = getAllPolarStatesRelatedToAPoint(w,h)
	print('len:',len(allPolarStates))
	#print([[eachPolarState.getRo(),eachPolarState.getTheta()] for eachPolarState in getAllPolarStatesRelatedToAPoint(w,h)])
	#print('\n\n')
	#print('walls:')
	#allWallStates = getAllCartesianStatesRelatedToWalls(w,h,3)
	#state = states.CartesianState(0,0)
	
	print('lineOfSight:')
	entities = [-1,0,1,2]
	strengthLineOfSight2 = 'low'
	range_ = 1
	allStatesLineOfSight = generateAllStatesLineOfSight(range_,strengthLineOfSight2,entities)
	getLineOfSight(w,h,strengthLineOfSight,state_,direction,env,range_)
	actions = 3
	directions_ = 1
	print('len:',len(allStatesLineOfSight))
	print('\ntotal states:',len(allPolarStates)*len(allStatesLineOfSight)*actions)
	#print(allStatesLineOfSight)

	#print([eachDistance for eachDistance in getDistancesRelatedToAPoint(3,3,1)])

#test()
'''