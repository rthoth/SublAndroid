class Emitter(object):

    listeners = None

    def on(self, evt, func):
        if self.listeners is None:
            self.listeners = {}

        if evt not in self.listeners:
            self.listeners[evt] = []

        self.listeners[evt].append(func)

    def off(self, evt, func):
        if self.listeners is not None and evt in self.listeners:
            self.listeners[evt].remove(func)
            if not self.listeners[evt]:
                del self.listeners[evt]
                if not self.listeners:
                    delattr(self, 'listeners')

    def fire(self, evt, **kwargs):
        if self.listeners is not None and evt in self.listeners:
            listeners = self.listeners.copy()
            for func in listeners[evt].copy():
                func(**kwargs)
