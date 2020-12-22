import os, sys
from setuptools import setup, find_packages

from smspilot import __version__

requirements = [
    'attrs==20.3.0',
    'certifi==2020.12.5',
    'chardet==4.0.0',
    'click==7.1.2',
    'colorama==0.4.4',
    'commonmark==0.9.1',
    'idna==2.10',
    'importlib-metadata==3.3.0',
    'prettytable==2.0.0',
    'profig==0.5.1',
    'prompt-toolkit==3.0.8',
    'Pygments==2.7.3',
    'pyperclip==1.8.1',
    'pyreadline==2.1',
    'questionary==1.9.0',
    'requests==2.25.1',
    'rich==9.5.1',
    'sms-pilot-py==0.2',
    'typing-extensions==3.7.4.3',
    'urllib3==1.26.2',
    'wcwidth==0.2.5',
    'zipp==3.4.0'
]

if sys.version.startswith("2.6"):
    requirements.append("argparse==1.3.0")

setup(
    name="SmsPilot CLI",
    version=".".join(map(str, __version__)),
    description="A command-line utility to interact with SmsPilot.ru API",
    url='https://github.com/migelbd/smspilot-cli',
    license='MIT',
    author='Mikhail Badrazhan',
    author_email='migel.bd@gmail.com',
    packages=['smspilot'],
    include_package_data=True,
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires=requirements,
    tests_require=[],
    entry_points={
        'console_scripts': [
            'smspilot = smspilot.main:main',
        ]
    }
)
