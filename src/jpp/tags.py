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
        
    def __str__(self):
        return "%s(%s)" % (self.__class__.__name__, str(self.value))

    def __repr__(self):
        return self.__str__()
        
        
    def __eq__(self,other):
        return self.value == other.value

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
    :retrun: Tag of Data or Verbatim type.
    :rtype: Tag
    """
    assert istag(line)
    line = line[2:]
    # is date?
    if len([d for d in line if d in '0123456789']) == 8:
        return Date(dt.date(int(line[:4]),int(line[4:6]),int(line[6:])))
    # make Multi tag
    return Multi([Verbatim(line)])
    
    
