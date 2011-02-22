import os.path
from zope.testing import doctest
from zope.app.testing import functional

ftesting_zcml = os.path.join(os.path.dirname(__file__), 'ftesting.zcml')
FunctionalLayer = functional.ZCMLLayer(ftesting_zcml, __name__,
                                       'FunctionalLayer')

def FunctionalDocTestSuite(module=None, **kw):
    module = doctest._normalize_module(module)
    suite = functional.FunctionalDocTestSuite(module, **kw)
    suite.layer = FunctionalLayer
    return suite

def FunctionalDocFileSuite(path, **kw):
    suite = functional.FunctionalDocFileSuite(path, **kw)
    suite.layer = FunctionalLayer
    return suite

class FunctionalTestCase(functional.FunctionalTestCase):
    layer = FunctionalLayer
