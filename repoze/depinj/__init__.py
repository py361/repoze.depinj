from zope.interface import Interface
from zope.interface import implements

class IDependencyInjector(Interface):
    """ """
    def inject_factory(fixture, real):
        """ Inject a testing dependency factory.  ``fixture`` is the
        factory used for testing purposes.  ``real`` is the actual
        factory implementation when the system is not used under test."""

    def inject(fixture, real):
        """ Inject a testing dependency object.  ``fixture`` is the
        object used for testing purposes.  ``real`` is the
        actual object when the system is not used under test."""

    def construct(real, *arg, **kw):
        """ Return the result of a testing factory related to ``real``
        when the system is under test or the result of the ``real``
        factory when the system is not under test.  ``*arg`` and
        ``**kw`` will be passed to either factory."""

    def lookup(real):
        """ Return a testing object related to ``real`` if the system
        is under test or the ``real`` when the system is not under
        test."""

class DependencyInjector(object):
    implements(IDependencyInjector)
    def __init__(self):
        self.factories = {}
        self.nonfactories = {}
        self.results = {}

    def inject_factory(self, fixture, real):
        self.factories[real] = fixture
        def promise():
            return self.results[real]
        return promise

    def inject(self, fixture, real):
        self.nonfactories[real] = fixture

    def construct(self, real, *arg, **kw):
        if real in self.factories:
            fake = self.factories[real]
            result = fake(*arg, **kw)
            self.results[real] = result
            return result
        return real(*arg, **kw)

    def lookup(self, real):
        if real in self.nonfactories:
            fake = self.nonfactories[real]
            return fake
        return real

