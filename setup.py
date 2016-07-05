import sys
from distutils.core import setup

if sys.version_info[0] < 3:
    version = str(sys.version_info[0]) + '.' + str(sys.version_info[1])
    sys.exit("""
    Sorry! Your Python version is %s, but this program requires at least
    Python 3. Please upgrade your Python installation, or try using pip3
    instead of pip.""" % version)

setup(
    name='corpus-downloader',
    packages = ['corpus'], # this must be the same as the name above
    py_modules=['corpus'],
    version='0.1.0',
    description = 'A downloader for textual corpora, for use in digital humanities, corpus linguistics, and natural language processing.',
    author = 'Jonathan Reeve',
    author_email = 'jon.reeve@gmail.com',
    url = 'https://github.com/DH-Box/corpus-downloader',
    download_url = 'https://github.com/DH-Box/corpus-downloader/tarball/0.1.0',
    include_package_data=True,
    keywords = ['nlp', 'text-analysis', 'corpora'],
    install_requires=[
        'click','pandas','pyyaml','sh'
    ],
    entry_points='''
        [console_scripts]
        corpus=corpus.corpus:cli
    ''',
)
