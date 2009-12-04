class DependencyInjector(object):
    def __init__(self):
        self.factories = {}
        self.lookups = {}
        self.factory_results = {}
        self.has_injections = False

    def inject_factory(self, fixture, real):
        self.factories[real] = fixture
        self.has_injections = True
        def promise():
            return self.factory_results[real]
        return promise

    def inject(self, fixture, real):
        self.has_injections = True
        self.lookups[real] = fixture

    def construct(self, real, *arg, **kw):
        if real in self.factories:
            fake = self.factories[real]
            result = fake(*arg, **kw)
            self.factory_results[real] = result
            return result
        return real(*arg, **kw)

    def lookup(self, real):
        if real in self.lookups:
            fake = self.lookups[real]
            return fake
        return real

    def clear(self):
        self.__init__()

injector = DependencyInjector()

def lookup(real):
    """ Return a testing object related to ``real`` if the system
    is under test or the ``real`` when the system is not under
    test."""
    if injector.has_injections:
        return injector.lookup(real)
    return real

def construct(real, *arg, **kw):
    """ Return the result of a testing factory related to ``real``
    when the system is under test or the result of the ``real``
    factory when the system is not under test.  ``*arg`` and
    ``**kw`` will be passed to either factory."""
    if injector.has_injections:
        return injector.construct(real, *arg, **kw)
    return real(*arg, **kw)

def inject_factory(fixture, real):
    """ Inject a testing dependency factory.  ``fixture`` is the
    factory used for testing purposes.  ``real`` is the actual
    factory implementation when the system is not used under test."""
    promise = injector.inject_factory(fixture, real)
    return promise

def inject(fixture, real):
    """ Inject a testing dependency object.  ``fixture`` is the
    object used for testing purposes.  ``real`` is the
    actual object when the system is not used under test."""
    return injector.inject(fixture, real)

def clear():
    """ Clear the dependency injection registry """
    injector.clear()

