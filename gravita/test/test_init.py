import unittest
from pyramid import testing


class InitTestCase(unittest.TestCase):

    def test_main(self):
        from gravita import main
        config = main(None, _config_factory=TestConfigFactory, foo='bar')
        self.assertTrue(isinstance(config, TestConfigFactory))
        self.assertTrue(config.wsgi_app_made)
        self.assertEqual(config.settings, {'foo': 'bar'})
        self.assertEqual(config.scanned, 'gravita')


class TestConfigFactory(object):

    def __init__(self, settings):
        self.settings = settings
        self.wsgi_app_made = False
        self.scanned = None

    def scan(self, what):
        self.scanned = what

    def make_wsgi_app(self):
        self.wsgi_app_made = True
        return self
