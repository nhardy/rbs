class Room:
  def __init__(self, faculty=None, capacity=20, resources=None, rid=None):
  	self.faculty = faculty
  	self.capacity = capacity
  	self.resources = resources
  	self.rid = rid
  	if self.rid is None:
  		#INSERT INTO DATABASE
  		self.rid = 0
  def