from mdjpp.tags import istag, maketag
from mdjpp.tags import Tag, Date, Verbatim, NoTag, Multi, Global, Time
from mdjpp.render import sstr, Null, HTML, MD
from mdjpp.options import default_options


################################################################################
# Parser
################################################################################

class JournalParser(object):

    def __init__(self):

        # list of open tags, starts with NoTag by default
        self.open_tags = [NoTag()]
        # last read tag that could be opened
        self.metastable_tag = None

        if default_options.mdjpp_null:
            self.engine = Null()
        elif default_options.mdjpp_md:
            self.engine = MD()
        elif default_options.mdjpp_html:
            self.engine = HTML()

        self.time_queue = []

    def __del__(self):
        self.finalize()

    @property
    def mtag(self):
        """
        :return: Metastable tag.
        """
        return self.metastable_tag

    @property
    def otag(self):
        """
        :return: Last open tag.
        """
        return self.open_tags[-1]

    @property
    def dtag(self):
        """
        :return: Current Date tag.
        """
        if isinstance(self.metastable_tag, Date):
            return self.metastable_tag
        for tag in self.open_tags[::-1]:
            if isinstance(tag, Date):
                return tag

    @property
    def ctag(self):
        """
        :return: Current tag.
        """
        if self.mtag is not None:
            return self.mtag
        if isinstance(self.otag, Date):
            if self.otag.last_tag is not None:
                return self.otag.last_tag
        return self.otag

    @property
    def ptag(self):
        """
        :return: Previous tag.
        """
        if self.mtag == self.otag:
            if self.dtag:
                if self.dtag.last_tag is not None:
                    return self.dtag.last_tag
        else:
            tagnr = 0
            if self.mtag is not None:
                tagnr += 1
            if isinstance(self.otag, Date):
                if self.otag.last_tag is not None:
                    tagnr += 1
                    if tagnr == 2:
                        return self.otag.last_tag
            tagnr += 1
            if tagnr == 2:
                return self.otag
            if len(self.open_tags) > 1:
                return self.open_tags[-2]

    def time_annotate_date(self, ttag):
        # Date tags
        if self.dtag:
            self.dtag.add_time(ttag)
            # add tag to the queue
            self.dtag.time_queue.append(ttag)
            self.time_annotate()

    def time_annotate(self):
        # Other tags (no Date tags) but Date tag was used
        if self.dtag:
            if not isinstance(self.ctag, Date):
                # if ctag is empty and ptag is not Date and has end it can be used as begin of ctag
                if self.ctag.isempty and self.ptag and not isinstance(self.ptag, Date) and self.ptag.end:
                    self.ctag.add_time(self.ptag.end)
                # last from queue might go to the previous tag if current tag is empty and has no begin
                if not isinstance(self.ptag, Date) and self.ctag.begin is None and self.ctag.isempty and self.ptag:
                    if len(self.dtag.time_queue):
                        self.ptag.add_time(self.dtag.time_queue[-1])
                # last from queue goes to current tag
                if len(self.dtag.time_queue):
                    self.ctag.add_time(self.dtag.time_queue.pop())

    def printable(self):
        # is current state printable?
        return True

    def printme_text(self, line):
        """
        Prints input line by submitting it to printme_text method of open tag.
        """
        self.otag.printme_text(line)

    def printme(self, line):
        """
        Prints input line by submitting it to printme method of open tag.
        """
        self.otag.printme(line)

    def open_tag(self, tag):
        """
        Opens submitted tag.
        """
        # is it global tag?
        if len(self.open_tags) == 1 and isinstance(tag, Multi):
            # is global if NoTag is only open tag and is of Multi type
            tag = Global(tag)
        # adds tag to open_tag list
        self.open_tags.append(tag)
        # time annotate
        self.time_annotate()
        # print tag opening if current state is printable
        if self.printable():
            # prints tag opener
            self.printme(self.engine.tag_opener(tag))
            # prints tag body
            self.printme(self.engine.tag(tag))

    def close_tag(self, tag):
        # check if tag closes last tag(s)
        # only if there are open tags
        if self.open_tags:
            # if tag is of the same type as otag?
            if isinstance(tag, type(self.otag)):
                closed_printable = False
                if self.printable():
                    self.printme(self.engine.tag_closer(self.otag))
                    closed_printable = True
                closed_tag = self.open_tags.pop(-1)
                if self.printable() and closed_printable:
                    self.printme(closed_tag)
            elif isinstance(tag, Date) and Date in list(map(type, self.open_tags)):
                while True:
                    closed_printable = False
                    if self.printable():
                        self.printme(self.engine.tag_closer(self.otag))
                        closed_printable = True
                    closed_tag = self.open_tags.pop(-1)
                    if self.printable() and closed_printable:
                        self.printme(closed_tag)
                    # if isinstance(closed[-1],Date):
                    if isinstance(closed_tag, Date):
                        break

    def proceed(self, source):
        """
        Proceeds with source, line by line.
        """

        for line in source:
            line = line.rstrip()
            if istag(line) and isinstance(maketag(line), Time):  # here, handle Time tags
                self.time_annotate_date(maketag(line))  # annotate Date tag and queue Time tag
                if not default_options.mdjpp_time_propagate:
                    continue
            # not a tag!
            if not istag(line) or isinstance(maketag(line), Time):
                if self.metastable_tag:  # and len(line):
                    # open metastable tag
                    self.open_tag(self.metastable_tag)
                    self.metastable_tag = None
                # print line
                if self.printable():
                    self.printme_text(line)
            # tag!
            else:
                # make regular tag
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
                    if isinstance(self.metastable_tag, Date) or isinstance(this_tag, Date):
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

    def final_printout(self, tag):
        if default_options.mdjpp_time_annotate:
            tag.time_annotate()
        for line in tag.body:
            if isinstance(line, Tag):
                self.final_printout(line)
            else:
                if isinstance(line, sstr) and len(line) == 0:
                    continue
                print(line)


################################################################################
# Filtered parser
################################################################################

class JournalParserFilter(JournalParser):

    def printable(self):
        return self.is_tag_printable()

    def printme(self, line):
        if self.is_line_printable(line):
            self.otag.printme(line)

    def final_printout(self, tag):
        if self.skip_this_tag(tag):
            return
        return super().final_printout(tag)

    def skip_this_tag(self, tag):
        if default_options.mdjpp_date_skip_notags and isinstance(tag, Date):
            for line in tag.body:
                if isinstance(line, Tag):
                    return False
            return True
        if default_options.mdjpp_date_skip_empty and isinstance(tag, Date):
            if len([t for t in tag.body if not isinstance(t, sstr) and str(t).strip()]) == 0:
                return True
        return False

    def is_tag_printable(self):
        if default_options.mdjpp_date_from or default_options.mdjpp_date_to:
            date_tag = [tag for tag in self.open_tags if isinstance(tag, Date)]
            if date_tag:
                date_tag = date_tag[0]
                if not default_options.mdjpp_date_from:
                    if not date_tag.value <= default_options.mdjpp_date_to:
                        return False
                elif not default_options.mdjpp_date_to:
                    if not date_tag.value >= default_options.mdjpp_date_from:
                        return False
                elif not date_tag.value <= default_options.mdjpp_date_to and date_tag.value >= default_options.mdjpp_date_from:
                    return False
        if default_options.mdjpp_skip_tag:
            for tag in (tag for tag in self.open_tags if isinstance(tag, Multi)):
                for tag_tag in tag.value:
                    if tag_tag.value in default_options.mdjpp_skip_tag:
                        return False
        if default_options.mdjpp_only_tag:
            if len(self.open_tags) >= 2 and isinstance(self.open_tags[-2], Date) and isinstance(self.otag, Multi):
                for tag in self.otag.value:
                    if tag.value in default_options.mdjpp_only_tag:
                        break
                else:
                    return False
        if default_options.mdjpp_only_global_tag:
            if len(self.open_tags) >= 2 and isinstance(self.open_tags[1], Multi):
                for tag in self.open_tags[1].value:
                    if tag.value in default_options.mdjpp_only_global_tag:
                        break
                else:
                    return False

        return True

    def is_line_printable(self, line):
        if not isinstance(line, Tag) and not isinstance(line, sstr):
            # skip_notag_content
            if default_options.mdjpp_skip_notag_content and isinstance(self.otag, NoTag):
                return False
            # skip_global_tag_content
            if default_options.mdjpp_skip_global_tag_content and len(self.open_tags) == 2 and isinstance(self.otag,
                                                                                                         Multi):
                return False
            # skip out of tag if only_tag is uesd
            if isinstance(self.otag, Date):
                if default_options.mdjpp_only_tag:
                    return False

        return True
