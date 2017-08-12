# Corpus: A Textual Corpus Downloader for Digital Humanities

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

### List only corpora containing texts in a certain language: 

```
$ corpus list --languages deu
                                                title      languages
shortname                                                           
dta        Deutsches Textarchiv (German Text Archive)            deu
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

## Installing

Since this is a command-line program, you'll need a Linux-style command line to run it. So if you run Windows, you'll first need to install a Linux-like environment like Ubuntu for Windows or Cygwin. 

This program is now on PyPi. You can install it by running: 

```
sudo pip3 install corpus-downloader
```

Alternatively, you can clone this repository (*recursively*, so you get the corpus list, too), change into this program’s directory and install it with pip3. (Make sure you have pip3, the python package manager for Python 3 installed first.) 

```
git clone --recursive https://github.com/DH-Box/corpus-downloader
cd corpus-downloader
pip3 install .
```

## Using on DH Box

You can also use `corpus-downloader` on [DH Box](http://dhbox.org), the Digital Humanities cloud workstation platform. Just spin up a new DH Box, log in, and click the "command line" tab. Then log in to the command line and run `sudo pip3 install corpus-downloader`. Now you can run `corpus list` and `corpus download` to download textual corpora.
