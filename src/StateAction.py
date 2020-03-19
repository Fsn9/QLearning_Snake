class StateAction():
	
	def __init__(self,state,action):
		self.state = state
		self.action = action
		self.Q = 0

	def getState(self):
		return self.state
	def getAction(self):
		return self.action
	def getQ(self):
		return self.Q
	def setQ(self,newQ):
		self.Q = newQ



