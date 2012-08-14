from setuptools import setup, find_packages

setup(
    name='django-fiber-multilingual',
    version=__import__('fiber').__version__,
    license='Apache License, Version 2.0',

    install_requires=[
        'PIL>=1.1.7',
        'django-piston==0.2.3',
        'django-mptt==0.5.2',
        'django-compressor>=0.7.1',
    ],
    dependency_links=['https://bitbucket.org/jespern/django-piston/get/7c90898072ce.tar.gz#egg=django-piston-0.2.3'],

    description='Django Fiber - a simple, user-friendly CMS for all your Django projects',
    long_description=open('README.rst').read(),

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
