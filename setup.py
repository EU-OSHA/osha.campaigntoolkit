from setuptools import setup, find_packages
import os

version = '1.0.6.dev0'
long_description = \
    open("README.txt").read() + "\n" + \
    open(os.path.join("docs", "HISTORY.txt")).read()

setup(name='osha.campaigntoolkit',
      version=version,
      description="EU-OSHA Campaign Toolkit",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          "Programming Language :: Python",
      ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['osha'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.api',
          'plone.app.dexterity [grok]',
          'z3c.jbot',
          'Products.LoginLockout',
          'Products.PasswordStrength',
          'mfabrik.webandmobile',
      ],
      extras_require={
          # list libs needed for testing this project
          'test': [
              'mock',
              'plone.app.testing',
              'unittest2',
          ]
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
