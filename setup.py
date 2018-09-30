from setuptools import find_packages
from setuptools import setup


setup(
    name='apex_pre_commit_hooks',
    description='i don\'t care.',
    version='0.1.0',

    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],

    packages=find_packages('.', exclude=('tests*', 'testing*')),
    install_requires=[
        'jsonschema',
        'mock',
        'pyyaml',
        'six',
    ],
    entry_points={
        'console_scripts': [
            'pre-commit-regex-me = apex_pre_commit.format_me:main',
        ],
    },
)