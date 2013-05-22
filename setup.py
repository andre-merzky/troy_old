
__author__    = "Andre Merzky"
__copyright__ = "Copyright 2012-2013, The SAGA Project"
__license__   = "LGPL3"


""" Setup script. Used by easy_install and pip. """

import os
import sys

from distutils.core                 import setup
from distutils.command.install_data import install_data
from distutils.command.sdist        import sdist

version = "latest"

try:
    cwd = os.path.dirname(os.path.abspath(__file__))
    fn = os.path.join(cwd, 'troy/VERSION')
    version = open(fn).read().strip()
except IOError:
    from subprocess import Popen, PIPE, STDOUT
    import re

    VERSION_MATCH = re.compile(r'\d+\.\d+\.\d+(\w|-)*')

    try:
        p = Popen(['git', 'describe', '--tags', '--always'],
            stdout=PIPE, stderr=STDOUT)
        out = p.communicate()[0]

        if (not p.returncode) and out:
            v = VERSION_MATCH.search(out)
            if v:
                version = v.group()
    except OSError:
        pass

scripts = []

# check python version. we need > 2.5
if sys.hexversion < 0x02050000:
    raise RuntimeError("TROY requires Python 2.5 or higher")


class our_install_data(install_data):

    def finalize_options(self):
        self.set_undefined_options('install',
            ('install_lib', 'install_dir'),
        )
        install_data.finalize_options(self)

    def run(self):
        install_data.run(self)
        # ensure there's a bliss/VERSION file
        fn = os.path.join(self.install_dir, 'troy', 'VERSION')
        open(fn, 'w').write(version)
        self.outfiles.append(fn)


class our_sdist(sdist):

    def make_release_tree(self, base_dir, files):
        sdist.make_release_tree(self, base_dir, files)
        # ensure there's a air/VERSION file
        fn = os.path.join(base_dir, 'troy', 'VERSION')
        open(fn, 'w').write(version)

setup_args = {
    'name':             "troy",
    'version':          version,
    'description':      "TROY",
    'long_description': "TROY",
    'author':           "Andre Merzky",
    'author_email':     "andre@merzky.net",
    'maintainer':       "Andre Merzky",
    'maintainer_email': "andre@merzky.net",
    'url':              "http://saga-project.github.com/troy/",
    'license':          "MIT",
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'License :: OSI Approved :: LGPL3',
        'Topic :: System :: Distributed Computing',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix'
    ],
    'packages': [
        "troy",
        "troy.engine",
        "troy.interface",
        "troy.adaptors",
    ],
    'package_data': {'': ['*.sh']},
    'zip_safe':     False,
    'scripts':      scripts,
    'data_files':   [("troy", [])],
    'cmdclass': {
        'install_data': our_install_data,
        'sdist':        our_sdist
    }
}

setup (**setup_args)

