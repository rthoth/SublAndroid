import sublime


class Highlight(object):
    def __init__(self, source, file, line, kind, what, how):
        self.source = source
        self.file = file
        self.line = line
        self.kind = kind
        self.what = what
        self.how = how


class Highlighter(object):
    def __init__(self, window):
        self.window = window
        self.highlights = {}

    def add_highlight(self, highlight):
        file = highlight.file

        if file not in self.highlights:
            self.highlights[file] = []

        self.highlights[file].append(highlight)

    def add_highlights(self, highlights, update=False):
        for highlight in highlights:
            self.add_highlight(highlight)

        if update:
            self.update()

    def remove_source(self, source, update=False):
        for file, highlights in self.highlights.items():
            


        if update:
            self.update()

    def update(self):
        for view in self.window.views():
            file = view.file_name()
            if file and file in self.highlights:
                self.update_view(view, self.highlights[file])

    def update_view(self, view, highlights):
        sublime.message_dialog(str(len(highlights)))
        for highlight in highlights:
            pass
