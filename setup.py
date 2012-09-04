from setuptools import setup, find_packages

name = 'auf.django.saml'
version = '1.6'

setup(name=name,
      version=version,
      description="Package to deal with our Identity Provider",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='Django SAML Auth',
      author='Olivier Larchev\xc3\xaaque',
      author_email='olivier.larcheveque@auf.org',
      url='http://pypi.auf.org/%s' % name,
      license='GPL',
      namespace_packages = ['auf', 'auf.django', ],
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
