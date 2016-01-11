from setuptools import setup

setup(
    name='corpus-downloader',
    version='0.1',
    py_modules=['corpus'],
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        corpus=corpus:cli
    ''',
)
