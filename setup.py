from sys import version_info
from setuptools import setup, find_packages

kwargs = {
    'name': 'django-yacapp',
    'version': '0.1',
    'description': 'A simple yet flexible ajax commenting system.',
    'author': 'Derrick Petzold',
    'author_email': 'dpetzold@gmail.com',
    'url': 'http://github.com/dpetzold/django-yacapp/',
    'keywords': 'django,ajax,comments',
    'license': 'BSD',
    'packages': [
        'yacapp',
    ],
    'include_package_data': True,
    'zip_safe': False,
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
}
setup(**kwargs)
