""" Setup script
"""


import setuptools


PROJECT = 'pmpc'

VERSION = '0.0.0'

AUTHOR = 'sinoroc'

INSTALL_REQUIREMENTS = [
    'pypiwin32',
    'python-mpd2'
]

ENTRY_POINTS = {
    'console_scripts': [
        'pmpc = pmpc.script:main',
    ]
}

SETUP_REQUIREMENTS = [
    'setuptools-pep8',
    'setuptools-lint'
]

PACKAGES = setuptools.find_packages()


setuptools.setup(
    name=PROJECT,
    version=VERSION,
    author=AUTHOR,
    packages=PACKAGES,
    entry_points=ENTRY_POINTS,
    install_requires=INSTALL_REQUIREMENTS,
    setup_requires=SETUP_REQUIREMENTS,
)


# EOF
