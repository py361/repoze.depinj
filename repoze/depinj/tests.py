import unittest
from repoze.depinj import clear

class TestDependencyInjector(unittest.TestCase):
    def _makeOne(self):
        from repoze.depinj import DependencyInjector
        return DependencyInjector()

    def test_ctor(self):
        injector = self._makeOne()
        self.assertEqual(injector.factories, {})
        self.assertEqual(injector.lookups, {})
        self.assertEqual(injector.factory_results, {})

    def test_inject_factory(self):
        injector = self._makeOne()
        promise = injector.inject_factory(DummyFactory, Dummy)
        injector.factory_results[Dummy] = 'abc'
        self.assertEqual(promise(), 'abc')

    def test_inject(self):
        injector = self._makeOne()
        injector.inject(Dummy, Dummy2)
        self.assertEqual(injector.lookups[Dummy2], Dummy)

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
        injector.lookups[Dummy] = Dummy2
        result = injector.lookup(Dummy)
        self.assertEqual(result, Dummy2)
        
    def test_lookup_notinjected(self):
        injector = self._makeOne()
        result = injector.lookup(Dummy)
        self.assertEqual(result, Dummy)

class Test_lookup(unittest.TestCase):
    def setUp(self):
        clear()

    def tearDown(self):
        clear()

    def test_it_injected(self):
        from repoze.depinj import lookup
        from repoze.depinj import injector
        injector.inject('123', 'whatever')
        self.assertEqual(lookup('whatever'), '123')
        
    def test_it_not_injected(self):
        from repoze.depinj import lookup
        self.assertEqual(lookup('whatever'), 'whatever')
        
class Test_construct(unittest.TestCase):
    def setUp(self):
        clear()

    def tearDown(self):
        clear()

    def test_it_injected(self):
        from repoze.depinj import construct
        from repoze.depinj import injector
        promise = injector.inject_factory(DummyFactory, 'whatever')
        self.assertEqual(construct('whatever', 'a', b=1).__class__,DummyFactory)
        fixture = promise()
        self.assertEqual(fixture.arg, ('a',))
        self.assertEqual(fixture.kw, {'b':1})
        
    def test_it_not_injected(self):
        from repoze.depinj import construct
        self.assertEqual(construct(DummyFactory).__class__, DummyFactory)

class Test_inject_factory(unittest.TestCase):
    def setUp(self):
        clear()

    def tearDown(self):
        clear()

    def test_it(self):
        from repoze.depinj import inject_factory
        from repoze.depinj import injector
        promise = inject_factory(Dummy, DummyFactory)
        injector.factory_results[DummyFactory] = 'result'
        self.assertEqual(promise(), 'result')

class Test_inject(unittest.TestCase):
    def setUp(self):
        clear()

    def tearDown(self):
        clear()

    def test_it(self):
        from repoze.depinj import inject
        from repoze.depinj import injector
        inject(Dummy, DummyFactory)
        self.assertEqual(injector.lookups[DummyFactory], Dummy)

class DummyInjector(object):
    def __init__(self, constructed=None, looked_up=None, result=None):
        self.constructed = constructed
        self.looked_up = looked_up
        self.result = result

    def lookup(self, real):
        return self.looked_up

    def construct(self, real, *arg, **kw):
        self.construct_args = arg, kw
        return self.constructed

class Dummy(object):
    pass

class Dummy2(object):
    pass

class DummyFactory(object):
    def __init__(self, *arg, **kw):
        self.arg = arg
        self.kw = kw
        
