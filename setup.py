from setuptools import setup, find_packages

version = '2.0.0+ls'

def read(name):
    return open(name).read()

long_description = (read('README.rst') + '\n' + read('CHANGELOG.rst'))

install_requires = [
          # -*- Extra requirements: -*-
          'argparse==1.2.1',
          'erp5.util==0.4.70',
          'lxml==4.6.2',
          'paste==3.5.0',
          'pastedeploy==2.1.1',
          'pastescript[wsgiutils]==3.2.1',
          'psutil==5.5.1',
          'pypdf==1.13',
          'python-magic==0.4.24',
          'six==1.14.0',
          'wsgiserver==1.3',
          'wsgiutils==0.7.2',
          'zope.interface==5.2.0'
          ]

setup(name='cloudooo',
      version=version,
      description="XML-RPC document conversion server",
      long_description=long_description,
      classifiers=[
        "Topic :: System :: Networking",
        "Topic :: System :: Operating System Kernels :: Linux",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Natural Language :: English",
        "Framework :: Paste"],
      keywords='xmlrpc openoffice wsgi paste python',
      author='Gabriel M. Monnerat',
      author_email='gabriel@nexedi.com',
      url='https://lab.nexedi.com/nexedi/cloudooo.git',
      license='GPLv3+ with wide exception for FOSS',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      entry_points="""
      [paste.app_factory]
      main = cloudooo.paster_application:application
      [console_scripts]
      cloudooo_tester = cloudooo.bin.cloudooo_tester:main
      echo_cloudooo_conf = cloudooo.bin.echo_cloudooo_conf:main
      runCloudoooUnitTest = cloudooo.tests.runHandlerUnitTest:run
      """,
      )
