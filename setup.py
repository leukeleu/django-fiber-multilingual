import os
import sys
from setuptools import setup, find_packages

version = __import__('fiber').__version__

if sys.argv[-1] == 'publish':  # upload to pypi
    os.system("python setup.py register sdist upload")
    print "You probably want to also tag the version now:"
    print "  git tag -a %s -m 'version %s'" % (version, version)
    print "  git push --tags"
    sys.exit()

setup(
    name='django-fiber-multilingual',
    version=version,
    license='Apache License, Version 2.0',

    install_requires=[
        'Pillow==2.0.0',
        'django-mptt==0.5.5',
        'django-compressor==1.3',
        'djangorestframework==2.3.6',
        'django-multilingual-ds9==0.3.0.7',
    ],
    dependency_links=[
        'https://github.com/leukeleu/django-multilingual-ds9/tarball/0.3.0.7#egg=django-multilingual-ds9-0.3.0.7',
    ],

    description='Django Fiber - a simple, user-friendly CMS for all your Django projects',
    long_description=open('README.md').read(),

    author='Dennis Bunskoek',
    author_email='dbunskoek@leukeleu.nl',

    url='https://github.com/leukeleu/django-fiber-multilingual',
    download_url='https://github.com/leukeleu/django-fiber-multilingual/tarball/multilingual_2',

    packages=find_packages(),
    include_package_data=True,

    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
