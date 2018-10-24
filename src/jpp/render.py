import hashlib

from jpp.tags import Multi, Date

def auto_color(value):
    return hashlib.md5(value.encode('utf-8')).hexdigest()[:6]


class Engine(object):
        
    def hrme(self,line):
        return """
---

%s

---
""" % str(line)


    def tag_opener(self,tag):
        raise NotImplementedError("Method not implemented")
        
    def tag_closer(self,tag):
        raise NotImplementedError("Method not implemented")
    
    def tag(self,tag):
        if isinstance(tag,Date):
            return self.tag_date(tag)
        elif isinstance(tag,Multi):
            return self.tag_multi(tag)
    
    def tag_date(self,tag):
        raise NotImplementedError("Method not implemented")
        
    def tag_verbatim(self,tag):
        raise NotImplementedError("Method not implemented")
        
    def tag_multi(self,tag):
        raise NotImplementedError("Method not implemented")
    


class HTML(Engine):
        

    def tag_opener(self,tag):
        return """<div style="margin:20px;">"""
        
    def tag_closer(self,tag):
        return """</div>"""
        
    def tag_date(self,tag):
        return self.hrme("""<p><strong>%s</strong></p>""" % str(tag.value))
        
    def tag_verbatim(self,tag):
        color = auto_color(tag.value)
        return """<span style="border:1px solid black; color:#%s">%s</span>""" % (color,str(tag.value))
        
    def tag_multi(self,tag):
        return """<p>%s</p>""" % ' '.join(map(self.tag_verbatim,tag.value))
    
