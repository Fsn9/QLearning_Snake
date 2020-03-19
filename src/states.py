import Position as pos
class PolarState():
	ro = 0
	theta = 0
	def __init__(self,ro,theta):
		self.ro = ro
		self.theta = theta
	def __str__(self):
		return ('ro:'+str(self.ro)+', theta:'+str(self.theta))
	def getRo(self):
		return self.ro
	def getTheta(self):
		return self.theta
	def setRo(self,ro):
		self.ro=ro
	def setTheta(self,theta):
		self.theta=theta
		
class CartesianState():
	position = []
	def __init__(self,x,y):
		self.position = pos.Position(x,y)
	def __str__(self):
		return ('CartesianState:'+' x='+str(self.position.getX())+', y='+str(self.position.getY()))
	def __sub__(self,other):
		return CartesianState(self.getPosition().getX()-other.getPosition().getX(),self.getPosition().getY()-other.getPosition().getY())
		
	def getPosition(self):
		return self.position
	def setPosition(self,pos):
		self.position=position
	def updatePosition(self,newX,newY):
		self.position.setX(newX)
		self.position.setY(newY)
	def getX(self):
		return self.position.getX()
	def getY(self):
		return self.position.getY()

