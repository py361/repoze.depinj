import unittest
from zope.testing.cleanup import cleanUp

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
        cleanUp()

    def tearDown(self):
        cleanUp()

    def test_it_injected(self):
        from repoze.depinj import IDependencyInjector
        from repoze.depinj import lookup
        from zope.component import getSiteManager
        injector = DummyInjector(looked_up='123')
        sm = getSiteManager()
        sm.registerUtility(injector, IDependencyInjector)
        self.assertEqual(lookup('whatever'), '123')
        
    def test_it_not_injected(self):
        from repoze.depinj import lookup
        self.assertEqual(lookup('whatever'), 'whatever')
        
class Test_construct(unittest.TestCase):
    def setUp(self):
        cleanUp()

    def tearDown(self):
        cleanUp()

    def test_it_injected(self):
        from repoze.depinj import IDependencyInjector
        from repoze.depinj import construct
        from zope.component import getSiteManager
        injector = DummyInjector(constructed='123')
        sm = getSiteManager()
        sm.registerUtility(injector, IDependencyInjector)
        self.assertEqual(construct('whatever', 'a', b=1), '123')
        self.assertEqual(injector.construct_args, (('a',), {'b':1}))
        
    def test_it_not_injected(self):
        from repoze.depinj import construct
        self.assertEqual(construct(DummyFactory).__class__, DummyFactory)

class Test_inject_factory(unittest.TestCase):
    def setUp(self):
        cleanUp()

    def tearDown(self):
        cleanUp()

    def test_it(self):
        from repoze.depinj import IDependencyInjector
        from repoze.depinj import inject_factory
        from zope.component import getSiteManager
        promise = inject_factory(Dummy, DummyFactory)
        sm = getSiteManager()
        injector = sm.getUtility(IDependencyInjector)
        injector.factory_results[DummyFactory] = 'result'
        self.assertEqual(promise(), 'result')

class Test_inject(unittest.TestCase):
    def setUp(self):
        cleanUp()

    def tearDown(self):
        cleanUp()

    def test_it(self):
        from repoze.depinj import IDependencyInjector
        from repoze.depinj import inject
        from zope.component import getSiteManager
        inject(Dummy, DummyFactory)
        sm = getSiteManager()
        injector = sm.getUtility(IDependencyInjector)
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
        
