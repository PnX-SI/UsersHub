
import re, os
import setuptools

from codecs import open


def get_version(path="VERSION"):
    """ Return the version of by with regex intead of importing it"""
    return open(path, "rt").read()

os.system('pip install git+https://github.com/PnX-SI/UsersHub-authentification-module@develop')

setuptools.setup(
    name='pypnusershub',
    version=get_version(),
    description="Python lib to authenticate using PN's UsersHub",
    long_description=open('README.rst', encoding="utf8").read().strip(),
    author="Les parcs nationaux de France",
    url='https://github.com/PnEcrins/UsersHub/',
    packages=setuptools.find_packages('usershub'),
    package_dir={'': 'usershub'},
    install_requires=list(open('requirements.txt', 'r')),
    include_package_data=True,
    zip_safe=False,
    keywords='ww',
    classifiers=['Development Status :: 1 - Planning',
                 'Intended Audience :: Developers',
                 'Natural Language :: English',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'License :: OSI Approved :: GNU Affero General Public License v3'
                 'Operating System :: OS Independent'],
)