class StateAction():
	state = []
	Q = 0
	action = 0
	
	def __init__(self,state,action):
		self.state = state
		self.action = action

	def getState(self):
		return self.state
	def getAction(self):
		return self.action
	def getQ(self):
		return self.Q
	def setQ(self,newQ):
		self.Q = newQ



