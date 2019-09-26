import hashlib
from functools import wraps
from os import linesep

from mdjpp.tags import Multi, Date, Global
from mdjpp import tagtag


def auto_color(value):
    return hashlib.md5(value.encode('utf-8')).hexdigest()[:6]


class sstr(str):
    pass


def ensure_sstr(gen):
    @wraps(gen)
    def patched(*args, **kwargs):
        obj = gen(*args, **kwargs)
        return None if obj is None else sstr(obj)

    return patched


class Null(object):
    null = None

    @ensure_sstr
    def tag_time(self, tag):
        return f"[{tag.begin}-{tag.end}]"

    @ensure_sstr
    def tag_opener(self, tag):
        return self.null

    @ensure_sstr
    def tag_closer(self, tag):
        return self.null

    @ensure_sstr
    def tag(self, tag):
        if isinstance(tag, Date):
            return self.tag_date(tag)
        elif isinstance(tag, Multi):
            return self.tag_multi(tag)

    @ensure_sstr
    def tag_date(self, tag):
        return tagtag + '%04d%02d%02d' % (tag.value.year, tag.value.month, tag.value.day)

    @ensure_sstr
    def tag_verbatim(self, tag):
        return tagtag + str(tag.value)

    @ensure_sstr
    def tag_multi(self, tag):
        return linesep.join(map(self.tag_verbatim, tag.value))


class MD(Null):

    @ensure_sstr
    def tag(self, tag):
        if isinstance(tag, Global):
            return self.tag_global(tag)
        else:
            return super().tag(tag)

    @ensure_sstr
    def tag_date(self, tag):
        return '## **%s**' % str(tag.value)

    @ensure_sstr
    def tag_verbatim(self, tag):
        return '**%s**' % str(tag.value)

    @ensure_sstr
    def tag_multi(self, tag):
        return "### " + '; '.join(map(self.tag_verbatim, tag.value))

    @ensure_sstr
    def tag_global(self, tag):
        return self.tag_multi(tag)[2:]


class HTML(Null):

    @ensure_sstr
    def hrme(self, line):
        return '***' + linesep * 2 + str(line) + linesep * 2 + '***'

    @ensure_sstr
    def tag_opener(self, tag):
        return """<div style="margin:1px;">"""

    @ensure_sstr
    def tag_closer(self, tag):
        return """</div>"""

    @ensure_sstr
    def tag_date(self, tag):
        return self.hrme("""<p><strong>%s</strong></p>""" % str(tag.value))

    @ensure_sstr
    def tag_verbatim(self, tag):
        color = auto_color(tag.value)
        return """<span style="border:1px solid black; color:#%s">
        <span style="margin-left: 3px; margin-right: 3px">%s</span></span>""" % (color, str(tag.value))

    @ensure_sstr
    def tag_multi(self, tag):
        return """<p>%s</p>""" % ' '.join(map(self.tag_verbatim, tag.value))
