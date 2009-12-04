class DependencyInjector(object):
    def __init__(self):
        self.factories = {}
        self.lookups = {}
        self.factory_results = {}

    def inject_factory(self, fixture, real):
        """ Inject a testing dependency factory.  ``fixture`` is the
        factory used for testing purposes.  ``real`` is the actual
        factory implementation when the system is not used under test."""
        def thunk():
            return self.factory_results[real]
        self.factories[real] = fixture
        return thunk

    def inject(self, fixture, real):
        """ Inject a testing dependency object.  ``fixture`` is the
        object used for testing purposes.  ``real`` is the
        actual object when the system is not used under test."""
        self.lookups[real] = fixture

    def construct(self, real, *arg, **kw):
        """ Return the result of a testing factory related to ``real``
        when the system is under test or the result of the ``real``
        factory when the system is not under test.  ``*arg`` and
        ``**kw`` will be passed to either factory."""
        if real in self.factories:
            fake = self.factories[real]
            result = fake(*arg, **kw)
            self.factory_results[real] = result
            return result
        return real(*arg, **kw)

    def lookup(self, real):
        """ Return a testing object related to ``real`` if the system
        is under test or the ``real`` when the system is not under
        test."""
        if real in self.lookups:
            fake = self.lookups[real]
            return fake
        return real

    def clear(self):
        """ Clear the dependency injection registry """
        self.__init__()

injector = DependencyInjector()
lookup = injector.lookup
construct = injector.construct
inject_factory = injector.inject_factory
inject = injector.inject
clear = injector.clear

