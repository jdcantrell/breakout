from math import floor, fabs
from Euclid import Segment

class CollisionGrid:
	def __init__(self, xWidth, yWidth):
		self.xWidth = xWidth
		self.yWidth = yWidth
		self.cells = {}
		self.items = {}

	def add(self,item,cell):
		if not self.cells.has_key(cell):
			self.cells[cell] = []
		if not self.items.has_key(item):
			self.items[item] = []

		self.cells[cell].append(item)
		self.items[item].append(cell)

	def addPoint(self, item, x, y):
		cell = (floor(x / self.xWidth), floor(y/self.yWidth))
		self.add(item,cell)
		return cell

	#Return all items that might be close to the x,y
	def getItems(self, x, y):
		cell = (floor(x / self.xWidth), floor(y/self.yWidth))
		if self.cells.has_key(cell):
			return self.cells[cell]
		else:
			return []

	def removeItem(self, item):
		if self.items.has_key(item):
			for cell in self.items[item]:
				self.cells[cell].remove(item)
			del self.items[item]

	#Add a list of points related to the item
	def addPoly(self, item, points):
		previousCell = None
		for point in points:
			cell = self.addPoint(item,point)
#need to test for intersections between possible cells
#the below code will not work properly in a lot of cases!
			if previousCell is not None:
				xDelta = fabs(previousCell[0] - cell[0])
				yDelta = fabs(previousCell[0] - cell[0])
				if xDelta > 1:	
					self.addCells(item,previousCell,cell, 0)
				if yDelta > 1:	
					self.addCells(item,previousCell,cell, 1)


	#Add multiple cells in a single line
	def addCells(self, item, startCell, endCell, idx):
		if startCell[idx] > endCell[idx]:
			start = endCell[idx] + 1
			end = startCell[idx]
		else:
			end = endCell[idx]
			start = startCell[idx] + 1

		while (start != end):
			if idx == 1:
				self.add(item, (startCell[0], start))
			else:
				self.add(item, (start, startCell[1]))
