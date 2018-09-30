from setuptools import setup

setup(
    name='pre_commit_apex',
    version='0.1.0',
    # py_modules=['pre_commit_regex_me'],
    entry_points={
        'console_scripts': [
            'pre_commit_regex_me = pre_commit_regex_me:main',
            'pre_commit_indent_me = pre_commit_indent_me:main',
        ]
    },
    install_requires=[
        'gitpython',
    ]
)
