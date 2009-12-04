import unittest

class TestDependencyInjector(unittest.TestCase):
    def _makeOne(self):
        from repoze.depinj import DependencyInjector
        return DependencyInjector()

    def test_ctor(self):
        injector = self._makeOne()
        self.assertEqual(injector.factories, {})
        self.assertEqual(injector.nonfactories, {})
        self.assertEqual(injector.results, {})

    def test_inject_factory(self):
        injector = self._makeOne()
        promise = injector.inject_factory(DummyFactory, Dummy)
        injector.results[Dummy] = 'abc'
        self.assertEqual(promise(), 'abc')

    def test_inject(self):
        injector = self._makeOne()
        injector.inject(Dummy, Dummy2)
        self.assertEqual(injector.nonfactories[Dummy2], Dummy)

    def test_construct_injected(self):
        injector = self._makeOne()
        injector.factories[Dummy] = DummyFactory
        result = injector.construct(Dummy, 'one', 'two', a=1, b=2)
        self.assertEqual(result.arg, ('one', 'two'))
        self.assertEqual(result.kw, {'a':1, 'b':2})

    def test_construct_not_injected(self):
        injector = self._makeOne()
        result = injector.construct(DummyFactory, 'one', 'two', a=1, b=2)
        self.assertEqual(result.arg, ('one', 'two'))
        self.assertEqual(result.kw, {'a':1, 'b':2})

    def test_lookup_injected(self):
        injector = self._makeOne()
        injector.nonfactories[Dummy] = Dummy2
        result = injector.lookup(Dummy)
        self.assertEqual(result, Dummy2)
        
    def test_lookup_notinjected(self):
        injector = self._makeOne()
        result = injector.lookup(Dummy)
        self.assertEqual(result, Dummy)

class Dummy(object):
    pass

class Dummy2(object):
    pass

class DummyFactory(object):
    def __init__(self, *arg, **kw):
        self.arg = arg
        self.kw = kw
        
