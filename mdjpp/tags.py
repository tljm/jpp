from mdjpp.options import makedate, maketime

class Tag(object):
    """
    Abstract tag.
    """
    def __init__(self,value):
        """
        :param value: Value of tag.
        """
        self.value = value
        self.body = []

        self.begin = None
        self.end = None
        
        self.isempty = True
        
    def __str__(self):
        return f"{self.__class__.__name__}({str(self.value)})"

    def __repr__(self):
        return self.__str__()
                
    def __eq__(self,other):
        if not isinstance(other,Tag):
            return False
        return self.value == other.value
        
    def printme_text(self,line):
        # this is meant for non technical prints
        if len(str(line).strip()):
            self.end = None
            self.isempty = False
        self.printme(line)
        
    def printme(self,line):
        return self.body.append(line)
        
    def add_time(self,ttag):
        
        if self.begin is not None or not self.isempty:
            self.end = ttag
            print('end',str(self),str(ttag))
        elif self.isempty:
            self.begin = ttag
            print('begin',str(self),str(ttag))
    


class NoTag(Tag):
    """
    No tag.
    """
    def __init__(self,dummy=None):
        """
        :param str dummy: Value of no tag.
        """
        super().__init__(dummy)
    

class Date(Tag):
    """
    Date tag.
    """
    def __init__(self,date):
        """
        :param datetime.date date: Date of this tag.
        """
        super().__init__(date)
        self.time_queue = []
        
    @property
    def last_tag(self):
        """
        :return Tag: Last tag in body, if any.
        """
        for line in self.body[::-1]:
            if isinstance(line,Tag):
                return line

class Time(Tag):
    """
    Time special tag.
    """
    def __init__(self,time):
        """
        :param datetime.time time: Time of this tag.
        """
        super().__init__(time)

    
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
        :param list tags: Tuple of :class:`Verbatim` tags.
        """
        super().__init__(tags)
    
    def append(self,tag):
        """
        :param tag: Verbatim or Mulit tag to add to the current tag.
        """
        if isinstance(tag,Verbatim):
            self.value.append(tag)
        elif isinstance(tag,Multi):
            self.value.extend(tag.value)


class Global(Multi):
    """
    Global Multiple verbatim tag.
    """
    def __init__(self,mtag):
        """
        :param class:`Multi` mtag: Input class:`Multi` tag.
        """
        super().__init__(mtag.value)
        


def istag(line):
    """
    :param str line: Input line to check
    :retrun: True if input line is a tag, i.e. starts with `@@`; otherwise returns False.
    :rtype: bool
    """
    return line.startswith('@@') and len(line)>2


def maketag(line):
    """
    :param str line: Input tag line.
    :return: Tag of Data, Time, or Verbatim type.
    :rtype: Tag
    """
    assert istag(line)
    line = line[2:]
    # is date?
    date = makedate(line)
    if date:
        return Date(date)
    # is time?
    time = maketime(line)
    if time:
        return Time(line)
    # make Multi tag
    return Multi([Verbatim(line)])
    
    
