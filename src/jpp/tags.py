import datetime as dt

class Tag(object):
    """
    Abstract tag.
    """
    def __init__(self,value):
	"""
	:param value: Value of tag.
	"""
	self.value = value
	self.body = None

class Date(Tag):
    """
    Date tag.
    """
    def __init__(self,date):
	"""
	:param datetime.date date: Date of this tag.
	"""
	super().__init__(date)
	
    
class Verbatim(Tag):
    """
    Verbaim tag.
    """
    def __init__(self,name):
	"""
	:param str name: Name of this tag.
	"""
	super().__init__(name)


class Multi(Tag):
    """
    Multiple verbatim tag.
    """
    def __init__(self,tags):
	"""
	:param tuple tags: Tuple of :class:`Verbatim` tags.
	"""
	super().__init__(tags)

