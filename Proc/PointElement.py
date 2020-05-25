class Point:

	def __init__(self,newx,newy):
		self.x = newx
		self.y = newy
	def Update(self , otherx , othery):
		self.x = otherx
		self.y = othery
	def __pow__(v, u):
		return u.y * v.x - u.x * v.y
	def mod(self):
		return pow(self.x ** 2 + self.y ** 2, 0.5)
	def __add__(v, u):
		return Point(v.x + u.x, v.y + u.y)
	def __sub__(v, u):
		return Point(v.x - u.x, v.y - u.y)
