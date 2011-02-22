from setuptools import setup, find_packages

setup(name='stiam.ro',

      # Fill in project info below
      version='0.1',
      description="",
      long_description="",
      keywords='',
      author='',
      author_email='',
      url='',
      license='',
      # Get more from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Programming Language :: Python',
                   'Environment :: Web Environment',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
                   'Framework :: Zope3',
                   ],

      packages=find_packages('src'),
      package_dir = {'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'elementtree',
                        'ZODB3',
                        'ZConfig',
                        'zdaemon',
                        'zope.publisher',
                        'zope.traversing',
                        'zope.app.wsgi>=3.4.0',
                        'zope.app.appsetup',
                        'zope.app.zcmlfiles',
                        # The following packages aren't needed from the
                        # beginning, but end up being used in most apps
                        'zope.annotation',
                        'zope.copypastemove',
                        'zope.formlib',
                        'zope.i18n',
                        'zope.app.authentication',
                        'zope.app.session',
                        'zope.app.intid',
                        'zope.app.keyreference',
                        'zope.app.catalog',
                        # Requires
                        'zope.viewlet',
                        'zope.contentprovider',
                        'zope.app.server',
                        'zope.app.apidoc',
                        'z3c.layer.minimal<=1.0.1',
                        'z3c.evalexception>=2.0',
                        'z3c.blobfile',
                        'Paste',
                        'PasteScript',
                        'PasteDeploy',
                        'BeautifulSoup',
                        'lovely.memcached<=0.1.4',
                        'z3c.indexer==0.6.0',
                        'zope.sendmail',
                        #'zc.async<=1.5.3',
                        'lovely.remotetask==0.5',
                        # The following packages are needed for functional
                        # tests only
                        'zope.testing',
                        'zope.app.testing',
                        'zope.app.securitypolicy',
                        # Allen
                        'allen.content.core',
                        'allen.content.section',
                        'allen.content.games',
                        'allen.content.jokes',
                        'allen.image.scale',
                        'allen.utils.cache',
                        'allen.catalog.timeline',
                        ],
      entry_points = """
      [console_scripts]
      stiamro-debug = stiamro.startup:interactive_debug_prompt
      stiamro-ctl = stiamro.startup:zdaemon_controller
      [paste.app_factory]
      main = stiamro.startup:application_factory
      """
      )
