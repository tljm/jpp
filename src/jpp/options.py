import datetime as dt


def makedate(line):
    if len([d for d in line if d in '0123456789']) == 8:
        return dt.date(int(line[:4]),int(line[4:6]),int(line[6:]))

class TagsFilters(object):
    
    jpp_skip_notag_content = False
    jpp_skip_global_tag_content = False
    
    jpp_date_from = ""
    jpp_date_to = ""
    
    jpp_date_skip_notags = False
    jpp_date_skip_empty = False
    
    jpp_skip_tag = ""
    jpp_only_tag = ""
    jpp_only_global_tag = ""

class JPP(TagsFilters):
    pass
    

    def reparse_options(self):
        
        # date
        if self.jpp_date_from:
            self.jpp_date_from = makedate(self.jpp_date_from)
        if self.jpp_date_to:
            self.jpp_date_to = makedate(self.jpp_date_to)

    
default_options = JPP()

