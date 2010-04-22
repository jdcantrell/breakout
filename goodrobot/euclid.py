class Vector:
	def __init__(self, point):
		self.x = point[0]
		self.y = point[1]
	
	def __sub__(self,vector):
		return Vector(self.x - vector.x, self.y - vector.y)

class Segment:
	def __init__(self, pt1, pt2):
		self.pt1 = Vector(pt1)
		self.pt2 = Vector(pt2)
	
	def collide(self, segment):
		#get segment vectors
		u = self.pt2 - self.pt1
		v = segment.pt2 - segment.pt1
		det = u.x * v.y - u.y * v.x

		#parallel
		if fabs(det) < .000000000001:
			return False
		
		#get vector between the pts
		w = self.pt1 - segment.pt1
		
		#Check if lines intersect but not within our segment
		s = v.x * w.y - v.y * w.x
		if det < 0:
			if s < det or s > 0:
				return False
		elif s < 0 or s > det:
			return False

		t = u.x * w.y - u.y * w.x
		if det < 0:
			if t < det or t > 0:
				return False
		elif t < 0 or t > det:
			return False

		return True
