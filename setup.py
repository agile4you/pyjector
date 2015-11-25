from codecs import open as codecs_open
from setuptools import setup, find_packages


with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='pyjector',
    version='0.0.1a1',
    description=u"Python Depedency Injection utilities.",
    long_description=long_description,
    classifiers=[],
    keywords='',
    author=u"Papavassiliou Vassilis",
    author_email=u"vpapavasil@email.com",
    url=u"repo/website link",
    license='GLPv3',
    packages=find_packages(exclude=['ez_setup', 'examples', 'test']),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'test': ['pytest'],
    }
)
