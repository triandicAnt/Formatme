from setuptools import setup

setup(
    name='pre_commit_regex_me',
    version='0.0.0',
    py_modules=['pre_commit_regex_me'],
    entry_points={'console_scripts': ['pre_commit_regex_me = pre_commit_regex_me:main']},
    install_requires=[
        'gitpython',
    ]
)
