import hashlib

from jpp.tags import Multi, Date

def auto_color(value):
    return hashlib.md5(value.encode('utf-8')).hexdigest()[:6]

def hrme(line):
    return """
---

%s

---
""" % str(line)

def tag_opener(tag):
    #return """<div style="margin:20px; border:1px solid black;">"""
    return """<div style="margin:20px;">"""
    
def tag_closer(tag):
    return """</div>"""
    
def tag_date(tag):
    return hrme("""<p><strong>%s</strong></p>""" % str(tag.value))
    
def tag_verbatim(tag):
    color = auto_color(tag.value)
    return """<span style="border:1px solid black; color:#%s">%s</span>""" % (color,str(tag.value))
    
def tag_multi(tag):
    return """<p>%s</p>""" % ' '.join(map(tag_verbatim,tag.value))
