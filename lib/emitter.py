class Emitter(object):

    listeners = None

    def on(self, evt, func, once=False):
        if self.listeners is None:
            self.listeners = {}

        if evt not in self.listeners:
            self.listeners[evt] = []

        self.listeners[evt].append(Listener(func, once))

    def once(self, evt, func):
        return self.on(evt, func, True)

    def off(self, evt, func):
        if self.listeners is not None and evt in self.listeners:
            self.listeners[evt].remove(func)

            if not self.listeners[evt]:
                del self.listeners[evt]
                if not self.listeners:
                    delattr(self, 'listeners')

    def fire(self, evt, *args):
        if self.listeners is not None and evt in self.listeners:
            listeners = self.listeners.copy()
            for listener in listeners[evt].copy():
                if listener.once:
                    self.off(evt, listener)
                listener.func(evt, *args)


class Listener(object):
    def __init__(self, func, once):
        self.func = func
        self.once = once

    def __eq__(self, other):
        return self.func == other.func if isinstance(other, Listener) else self.func == other
