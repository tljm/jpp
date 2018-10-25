from jpp.tags import istag, maketag
from jpp.tags import Tag,Date,Verbatim,NoTag,Multi
from jpp.render import HTML,sstr
from jpp.options import default_options


################################################################################
# Filters
################################################################################

class Filters(object):
    
    def is_tag_printable(self):
        if default_options.jpp_date_from or default_options.jpp_date_to:
            date_tag = [tag for tag in self.open_tags if isinstance(tag,Date)]
            if date_tag:
                date_tag = date_tag[0]
                if not default_options.jpp_date_from:
                    return date_tag.value <= default_options.jpp_date_to
                if not default_options.jpp_date_to:
                    return date_tag.value >= default_options.jpp_date_from
                return date_tag.value <= default_options.jpp_date_to and date_tag.value >= default_options.jpp_date_from
        return True

    def is_line_printable(self,line):
        if not isinstance(line,Tag) and not isinstance(line, sstr):
            # skip_notag_content
            if default_options.jpp_skip_notag_content and isinstance(self.otag,NoTag):
                return False
            # skip_global_tag_content
            if default_options.jpp_skip_global_tag_content and len(self.open_tags) == 2 and isinstance(self.otag,Multi):
                return False
        return True

################################################################################
# Parser
################################################################################

class JournalParser(Filters):
    
    def __init__(self):
        
        self.open_tags = [NoTag()]
        self.metastable_tag = None
        
        self.engine = HTML()
    
    def __del__(self):
        self.finalize()
    
    @property
    def otag(self):
        return self.open_tags[-1]
        
    def printable(self):
        return self.is_tag_printable()
    
    def print(self,line):
        if self.is_line_printable(line):
            self.otag.print(line)
        
    def open_tag(self,tag):
        self.open_tags.append(tag)
        # print tag opening if current state is printable
        if self.printable():
            self.print(self.engine.tag_opener(tag))
            self.print(self.engine.tag(tag))
        
    def close_tag(self,tag):
        # check is tag closes last tag(s)
        if self.open_tags:
            if isinstance(tag,type(self.otag)):
                closed_tag = self.open_tags.pop(-1)
                if self.printable():
                    self.print(closed_tag)
                    self.print(self.engine.tag_closer(closed_tag))
            elif isinstance(tag,Date) and Date in list(map(type,self.open_tags)):
                while True:
                    closed_tag = self.open_tags.pop(-1)
                    if self.printable():
                        self.print(closed_tag)
                        self.print(self.engine.tag_closer(closed_tag))
                    #if isinstance(closed[-1],Date):
                    if isinstance(closed_tag,Date):
                        break
        
    def proceed(self,source):
        """
        Proceed with source.
        """
        for line in source:
            line = line.rstrip()
            # not a tag!
            if not istag(line):
                if self.metastable_tag:
                    # open metastable tag
                    self.open_tag(self.metastable_tag)
                    self.metastable_tag = None
                # print line
                if self.printable():
                    self.print(line)
            # tag!
            else:
                this_tag = maketag(line)
                # no metastable tag
                if not self.metastable_tag:
                    # make new metastable tag
                    self.metastable_tag = this_tag
                    # does new tag close last tag?
                    self.close_tag(this_tag)
                # metastable tag present
                else:
                    # is metastable tag or this tag of Date type?
                    if isinstance(self.metastable_tag,Date) or isinstance(this_tag,Date):
                        # open metastable tag
                        self.open_tag(self.metastable_tag)
                        # recreate metastable tag with new tag
                        self.metastable_tag = this_tag
                        # does new tag close last tag?
                        self.close_tag(this_tag)
                    else:
                        # add new tag to metastable tag
                        self.metastable_tag.append(this_tag)
    
    def finalize(self):
        for tag in self.open_tags[:0:-1]:
            self.close_tag(tag)
        if self.open_tags:
            self.final_printout(self.open_tags.pop())
    
    def final_printout(self,tag):
        #print(tag)
        for line in tag.body:
            if isinstance(line,Tag):
                self.final_printout(line)
            else:
                print(line)


