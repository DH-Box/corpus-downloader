import click
import yaml
from pandas import DataFrame as df
from pandas import set_option as pandas_set_option
import sh
import logging
from pkg_resources import resource_filename

class Config(object):
    def __init__(self):
        """Gets the config file. Unless the user specifies something,
        this will be in the current directory."""

        # Get config file, whereever that is in the user's system. 
        config = resource_filename(__name__, 'config.yaml')

        try:
            self.config = open(config).read()
        except:
            raise click.ClickException("Couldn't find the config file from %s." % config)
        try:
            configDict = yaml.safe_load(self.config)
            self.listFilename = configDict['corpuslist']
            self.downloadTo = configDict['downloadTo']
        except:
            raise click.ClickException("Couldn't parse the config file. Is it in the right format?")

@click.group()
@click.option('--verbose', is_flag=True, help='Get extra information about what\'s happening behind the scenes.')
@click.option('--debug', is_flag=True, help='Turn on debugging messages.')
@click.version_option('0.1')
@click.pass_context
def cli(ctx, verbose, debug):
    """Corpus is a command line tool that lists and downloads textual corpora.

    This tool was originally created for use in the Digital Humanities
    toolbox called DHBox.
    """
    # Create a config object and remember it as as the context object.  From
    # this point onwards other commands can refer to it by using the
    # @pass_obj decorator.
    ctx.obj = Config()

    # This allows Pandas to display at the current terminal width.
    pandas_set_option('display.width', None)

    if verbose:
        logging.basicConfig(level=logging.INFO)

    if debug:
        logging.basicConfig(level=logging.DEBUG)

@cli.command()
@click.option('--centuries', help='Comma-separated list of centuries to display, e.g. 16th,17th.')
@click.option('--categories', help='Comma-separated list of categories to display, e.g. literature,classics.')
@click.pass_obj
def list(ctx, centuries, categories):
    """Lists corpora available for download."""
    logging.info('Running subcommand list().')
    click.echo(ctx.downloadTo)
    corpuslist = readCorpusList()
    fields = ['title', 'centuries', 'categories']
    showCorpusList(corpuslist, fields, centuries, categories)

@click.pass_obj
def readCorpusList(ctx):
    """Reads the corpus list from corpus-list.yaml (or other file specified in the config).
    Returns a pandas data frame.
    """
    try:
        # corpusList = open(ctx.listFilename).read()
        corpusListFile = resource_filename(__name__, 'corpus-list/corpus-list.yaml')
        corpusList = open(corpusListFile).read() 
    except:
        raise click.ClickException("Couldn't read the corpus list from %s." % corpusListFile)
    try:
        corpusListDict = yaml.safe_load(corpusList)
        corpusListDF = df(corpusListDict).set_index('shortname')
    except:
        raise click.ClickException("Couldn't parse the corpus list from %s. Is it in the right format?" % ctx.listFilename)

    return corpusListDF

def filterCorpusList(corpuslist, field, values):
    values = values.split(',')
    values = ('|').join(values) # Pandas format for OR statements is like "16th|17th"
    corpuslist = corpuslist[corpuslist[field].str.contains(values, na=False)]
    return corpuslist

def showCorpusList(corpusListDF, fields, centuries=None, categories=None):

    # Filter by default fields.
    table = corpusListDF[fields]

    if centuries is not None:
        table = filterCorpusList(table, 'centuries', centuries)

    if categories is not None:
        table = filterCorpusList(table, 'categories', categories)

    print(table)

@cli.command()
@click.argument('shortname')
@click.argument('destination', required=False)
@click.option('--markup', help='Comma-separated markup type(s), in case there are multiple markup types in a corpus. E.g. --markup TEI,HTML', required=False)
@click.pass_obj
def download(ctx, shortname, destination, markup=None):
    """Downloads a corpus.

    This will download the corpus with the given shortname into the
    download destination. If the download destination is not provided,
    this will automatically use the default download location, given
    by the config file.
    """

    # Check to make sure the requested corpus exists.
    corpusList = readCorpusList()
    if shortname not in corpusList.index.tolist():
        raise click.ClickException("Couldn't find the specified corpus. Are you sure you have the right shortname?")

    if destination is None:
        destination = ctx.downloadTo

    corpus = corpusList.ix[shortname]

    print(corpus)

    text = corpus.text

    # A convoluted way to check the type of the corpus text item,
    # but since we've redefined `list` above, we can't do `if type(corpus) is list`.
    if type(text) == type([]):
        # This means we have more than one text type, and we need to disambiguate.

        # Check to see whether the user has already specified the text.
        if markup is None:
            # If the user hasn't specified a text...
            markupTypes = ', '.join([textType['markup'] for textType in text])
            raise click.ClickException('There are %s text types in this corpus: %s. Please specify which one you want with the --markup flag.' % (len(text), markupTypes))

        # Make a list of markup types the user has specified. 
        markups = markup.split(',')

        for record in text: 
            print(record)
            if record['markup'] in markups: 
                url = record['url']
                click.echo('Downloading corpus %s of type %s to %s from URL %s.' % (shortname, record['markup'], destination, url))
                downloadFromRecord(record, url, destination)

    elif type(text['url']) == type([]):
        # This means we have one text type with several URLs.
        print(text)
        for url in text['url']:
            downloadFromRecord(text, url, destination)
    else:
        # We have only one text type.
        print(text)
        click.echo('Downloading corpus %s of type %s to %s.' % (shortname, text['markup'], destination))
        url = text['url']
        downloadFromRecord(text, url, destination)

def downloadFromRecord(record, url, destination):
    """ This helper function takes a markup record with the fields `url` and `file-format`,
    and downloads it according to its file type.
    """
    logging.info('\nDownloading from record: !\n', record)
    form = record['file-format']
    print('form: ', form)
    print('url: ', url)
    print(sh.cd(destination))
    if form == 'git':
        gitDownload(url, destination)
    if form == 'zip' or form == 'tar.gz':
        archiveDownload(url, destination, form)

def gitDownload(url, destination):
    print('Now git cloning from URL %s to %s' % (url, destination))
    print(sh.pwd())
    for line in sh.git.clone(url, '--progress', '--recursive', _err_to_out=True, _iter=True):
        print(line)
    return

def archiveDownload(url, destination, archiveType):
    logging.info('Now downloading archive file from URL %s to %s' % (url, destination))
    # No-clobber makes it so that it doesn't download existing files.
    for line in sh.wget(url, '--no-clobber', _err_to_out=True, _iter=True):
        print(line)
    filename = url.split('/')[-1]
    if archiveType == 'zip':
        logging.info('Unzipping zip file from: ', filename)
        sh.unzip(filename)
    elif archiveType == 'tar.gz':
        logging.info('Untarring tar.gz file from: ', filename)
        sh.tar('-xvzf', filename )
    logging.info('Removing archive file.')
    sh.rm(filename)
    return

if __name__ == '__main__':
    cli()
