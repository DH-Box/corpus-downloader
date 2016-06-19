#Corpus: A Textual Corpus Downloader for Digital Humanities

Corpus is a command-line textual corpus downloader, designed for use in the Digital Humanities. This program is useful for anyone that needs to download large amounts of text, say, for text analysis. Want to conduct a digital macroanalysis of all Shakespeare plays? How about a linguistic study of a news corpus? This tool helps you get those texts, so you spend less time online and more time with the analysis itself. 

Corpus handles downloading corpora from a few different protocols and file types. It does the equivalent of `git clone` (with recursive submodule checkout, as well) and `wget`, but also unzips and untars archives, simplifying the process of getting a corpus.

## Demo

### List all downloadable corpora: 

```
$ corpus list
                                                                title   centuries  categories
shortname                                                                                    
shc                                    Shakespeare His Contemporaries  16th, 17th  literature
folger-shakespeare           Folger Shakespeare Library Digital Texts  16th, 17th  literature
perseus-c-greek                               Perseus Canonical Greek         NaN    classics
stanford-1880s      Adult British Fiction of the 1880s, Assembled ...        19th  literature
reuters-21578                                           Reuters-21578         NaN     history
ecco-tcp            Eighteenth Century Collections Online / Text C...        18th  literature
```

### List only corpora with 18th century texts: 

```
$ corpus list --centuries 18th
                                                       title centuries  categories
shortname                                                                         
ecco-tcp   Eighteenth Century Collections Online / Text C...      18th  literature
```

### List only corpora from a certain discipline / category: 

```
$ corpus list --category classics

                                   title centuries categories
shortname                                                    
perseus-c-greek  Perseus Canonical Greek       NaN   classics
```

### Download a corpus: 

```
$ corpus download shc

authors                                                multiple
categories                                           literature
centuries                                            16th, 17th
homepage                                                    NaN
subcorpora                                                  NaN
text          {'markup': 'TEI-Simple', 'url': 'https://githu...
title                            Shakespeare His Contemporaries
url-source                                                  NaN
Name: shc, dtype: object

Downloading corpus shc of type TEI-Simple to /home/jon/corpora.

Now git cloning from URL https://github.com/JonathanReeve/corpus-SHC.git to /home/jon/corpora
/home/jon/corpora

Cloning into 'corpus-SHC'...
```

### Download Only Certain Markup Types from a Corpus

```
$ corpus download folger-shakespeare --markup TEI,HTML
```


## Available Functions and Options

From `corpus --help`: 

```

Usage: corpus.py [OPTIONS] COMMAND [ARGS]...

  Corpus is a command line tool that lists and downloads textual corpora.

  This tool was originally created for use in the Digital Humanities toolbox
  called DHBox.

Options:
  --verbose  Get extra information about what's happening behind the scenes.
  --debug    Turn on debugging messages.
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  download  Downloads a corpus.
  list      Lists corpora available for download.
```


## Configuring

Corpus reads a config file from config.yaml, which should be in the same directory as corpus.py. It has these configurable items: 

```
corpuslist: corpus-list/corpus-list.yaml   
downloadTo: ~/corpora
```

`corpuslist` is a path to the corpus catalog. You can add your own corpora here if you follow the YAML format of the existing entries. 

`downloadTo` is the destination location on your local machine, where the corpora will be downloaded.  

## Installing

Until this package shows up on Pypi, you can change into this program’s directory and run `pip3 install .`. (Make sure you have pip3, the python package manager for Python 3 installed first.) 

