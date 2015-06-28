from .emitter import Emitter
from .daemon import onlysuccess


class Java(Emitter):
    def __init__(self, gradle, daemon):
        self.gradle = gradle
        self.daemon = daemon

    def saved(self, javafile):
        self.daemon.send({'command': 'compileJava'}, self.on_java_compiled)

    @onlysuccess
    def on_java_compiled(self, java_result):
        if 'failures' in java_result:
            java_failures = [JavaFailure(failure['fileName'], failure['lineNumber'],
                             failure['kind'], failure['what'], failure['how'])
                             for failure in java_result['failures']]

            self.gradle.fire('java_compile_error', java_failures)


class JavaFailure(object):
    def __init__(self, file, line, kind, what, how):
        self.file = file
        self.line = line
        self.kind = kind
        self.what = what
        self.how = how
