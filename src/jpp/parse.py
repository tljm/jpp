from jpp.tags import istag, maketag
from jpp.tags import Date,Verbatim


class JournalParser(object):
    
    def __init__(self):
        
        self.open_tags = []
        self.metastable_tag = None
        
    def print(self):
        return True
        
    def proceed(self,source):
        """
        Proceed with source.
        """
        for line in source:
            line = line.rstrip()
            if not istag(line) and self.print():
                print(line)
            else:
                this_tag = maketag(line)
                if not self.metastable_tag:
                    self.metastable_tag = this_tag
                else:
                    if isinstance(self.metastable_tag,Date):
                        # open metastable tag
                        self.open_tags.append(self.metastable_tag)
                        self.metastable_tag = this_tag
                    else:
                        # is is date?
                        
                        
                
                
                print(maketag(line))
            
                
