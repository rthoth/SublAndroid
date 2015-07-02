from .emitter import Emitter
from .daemon import onlysuccess
from .highlight import Highlight


class JavaHighlight(Highlight):
    def __init__(self, *args):
        super(JavaHighlight, self).__init__('java', *args)


class Java(Emitter):
    def __init__(self, gradle, daemon):
        self.gradle = gradle
        self.daemon = daemon

    def saved(self, javafile):
        self.daemon.send({'command': 'compileJava'}, self.on_java_compiled)

    @onlysuccess
    def on_java_compiled(self, result):
        if 'failures' in result:
            highlights = [JavaHighlight(failure['fileName'], failure['lineNumber'],
                          failure['kind'], failure['what'], failure['how'])
                          for failure in result['failures']]
        else:
            highlights = []

        self.gradle.fire('java_highlights', highlights)
