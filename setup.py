import sys
from distutils.core import setup

setup(
    name='corpus-downloader',
    packages = ['corpus'], # this must be the same as the name above
    py_modules=['corpus'],
    version='0.1.11',
    description = 'A downloader for textual corpora, for use in digital humanities, corpus linguistics, and natural language processing.',
    author = 'Jonathan Reeve',
    author_email = 'jon.reeve@gmail.com',
    url = 'https://github.com/DH-Box/corpus-downloader',
    download_url = 'https://github.com/DH-Box/corpus-downloader/tarball/0.1.11',
    include_package_data=True,
    package_data = { 
        'corpus': ['corpus-list/corpus-list.yaml']
        },
    keywords = ['nlp', 'text-analysis', 'corpora'],
    install_requires=[
        'click','pandas','pyyaml','sh','wget'
    ],
    entry_points='''
        [console_scripts]
        corpus=corpus.corpus:cli
    ''',
)
