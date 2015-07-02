import sublime


class Highlight(object):
    def __init__(self, source, filename, line, kind, what, how):
        self.source = source
        self.filename = filename
        self.line = line
        self.kind = kind
        self.what = what
        self.how = how


class Highlighter(object):
    def __init__(self, window):
        self.window = window
        self.highlights = {}

    def add_highlight(self, highlight):
        filename = highlight.filename

        if filename not in self.highlights:
            self.highlights[filename] = []

        self.highlights[filename].append(highlight)

    def add_highlights(self, highlights, update=False):
        for highlight in highlights:
            self.add_highlight(highlight)

        if update:
            self.update()

    def create_region(self, highlight, view):
        line = view.line(view.text_point(highlight.line - 1, 0))
        region = view.find(highlight.how, line.begin(), sublime.LITERAL)
        if region is not None:
            return sublime.Region(region.begin(), line.end())
        else:
            line

    def flag(self, source, kind):
        return sublime.DRAW_NO_FILL

    def icon(self, source, kind):
        return 'dot'

    def remove_highlights(self, source):
        for filename, highlights in self.highlights.items():
            for index, highlight in list(enumerate(highlights))[::-1]:
                if highlight.source == source:
                    del highlights[index]

        for view in self.window.views():
            view.erase_regions('sublandroid-%s' % source)

    def scope(self, source, kind):
        return 'string'

    def update(self):
        for view in self.window.views():
            filename = view.file_name()
            if filename and filename in self.highlights:
                self.update_view(view, self.highlights[filename])

    def update_view(self, view, highlights):
        # regions = [self.create_region(highlight, view) for highlight in highlights]
        # view.add_regions('sublandroid', regions, 'constant.numeric', 'circle', sublime.DRAW_NO_OUTLINE)
        sources = {}
        for highlight in highlights:
            if highlight.source not in sources:
                sources[highlight.source] = {}

            kinds = sources[highlight.source]
            if highlight.kind not in kinds:
                kinds[highlight.kind] = []

            kinds[highlight.kind].append(highlight)

        for source, kinds in sources.items():
            for kind, highlights in kinds.items():
                regions = [self.create_region(highlight, view) for highlight in highlights]
                view.add_regions('sublandroid-%s' % source,
                                 regions, self.scope(source, kind),
                                 self.icon(source, kind), self.flag(source, kind))
