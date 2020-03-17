class Position():
	x = 0
	y = 0
	def __init__(self,x,y):
		self.x=x
		self.y=y
	def __sub__(self,other):
		return self.x-other.x,self.y-other.y
	def getX(self):
		return self.x
	def getY(self):
		return self.y
	def setX(self,x):
		self.x = x
	def setY(self,y):
		self.y = y