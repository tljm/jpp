from jpp.tags import istag, maketag
from jpp.tags import Date,Verbatim


class JournalParser(object):
    
    def __init__(self):
        
        self.open_tags = []
        self.metastable_tag = None
    
    def __del__(self):
        self.finalize()
    
    def print(self):
        return True
        
    def open_tag(self,tag):
        self.open_tags.append(tag)
        print("OPEN: %s" % tag)
        
    def close_tag(self,tag):
        closed = []
        if self.open_tags:
            if isinstance(tag,type(self.open_tags[-1])):
                closed.append(self.open_tags.pop(-1))
            elif isinstance(tag,Date) and Date in list(map(type,self.open_tags)):
                while True:
                    closed.append(self.open_tags.pop(-1))
                    if isinstance(closed[-1],Date):
                        break
        if closed:
            for c in closed:
                print("CLOSED: %s" % c)
        
    def proceed(self,source):
        """
        Proceed with source.
        """
        for line in source:
            line = line.rstrip()
            if not istag(line) and self.print():
                if self.metastable_tag:
                    self.open_tag(self.metastable_tag)
                    self.metastable_tag = None
                    print(self.open_tags)
                    
                print(line)
            else:
                this_tag = maketag(line)
                if not self.metastable_tag:
                    self.metastable_tag = this_tag
                    self.close_tag(this_tag)
                else:
                    if isinstance(self.metastable_tag,Date) or isinstance(this_tag,Date):
                        # open metastable tag
                        self.open_tag(self.metastable_tag)
                        self.metastable_tag = this_tag
                        self.close_tag(this_tag)
                    else:
                        self.metastable_tag.append(this_tag)
    
    def finalize(self):
        for c in self.open_tags[::-1]:
            print("CLOSED: %s" % c)
            
                
