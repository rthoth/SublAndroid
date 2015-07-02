class IPWindow(object):
    """Instance Peer Window"""

    @classmethod
    def instance(cls, window, instance=None):
        try:
            instances = cls.instances
        except:
            instances = cls.instances = {}

        id = str(window.id())
        old = instances[id] if id in instances else None

        if instance is not None:
            instances[id] = instance

        return old
