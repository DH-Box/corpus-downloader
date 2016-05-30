import click
import yaml
import pandas
import sh

class Config(object):
    def __init__(self, config='config.yaml'):
        """Gets the config file. Unless the user specifies something,
        this will be in the current directory."""
        try:
            self.config = open(config).read()
        except:
            raise click.ClickException("Couldn't find the config file!")
        try:
            configDict = yaml.safe_load(self.config)
            self.listFilename = configDict['corpuslist']
            self.downloadTo = configDict['downloadTo']
        except:
            raise click.ClickException("Couldn't parse the config file. Is it in the right format?")

@click.group()
@click.version_option('0.1')
@click.pass_context
def cli(ctx):
    """Corpus is a command line tool that lists and downloads textual corpora.

    This tool was originally created for use in the Digital Humanities
    toolbox called DHBox.
    """
    # Create a config object and remember it as as the context object.  From
    # this point onwards other commands can refer to it by using the
    # @pass_obj decorator.
    ctx.obj = Config()

    # This allows Pandas to display at the current terminal width.
    pandas.set_option('display.width', None)

@cli.command()
@click.option('--centuries', help='Comma-separated list of centuries to display, e.g. 16th,17th.')
@click.option('--categories', help='Comma-separated list of categories to display, e.g. literature,classics.')
@click.pass_obj
def list(ctx, centuries, categories):
    """Lists corpora available for download."""
    click.echo('Listing!')
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
        corpusList = open(ctx.listFilename).read()
    except:
        raise click.ClickException("Couldn't read the corpus list from %s." % ctx.listFilename)
    try:
        corpusListDict = yaml.safe_load(corpusList)
        corpusDict = {x['shortname']: x for x in corpusListDict}
        print(corpusDict)
        corpusListDF = pandas.DataFrame(corpusListDict).set_index('shortname')
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

        markups = markup.split(',')

        textDF = pandas.DataFrame(text)

        for markupType in markups:
            markupRecord = textDF[textDF.markup == markupType] # Get the record with our markup type.
            click.echo('Downloading corpus %s of type %s to %s.' % (shortname, markupType, destination))
            downloadFromRecord(markupRecord)
    elif type(text['url']) == type([]):
        # This means we have one text type with several URLs.
        markupRecord = pandas.DataFrame(text)
        print(markupRecord)
        for index, record in markupRecord.iterrows():
            downloadFromRecord(record, destination)

    else:
        # We have only one text type.
        print(text)
        click.echo('Downloading corpus %s of type %s to %s.' % (shortname, text['markup'], destination))
        markupRecord = pandas.DataFrame(text, index=[0]) # Pandas requires we pass an index here.
        downloadFromRecord(markupRecord, destination)

def downloadFromRecord(markupRecord, destination):
    """ This helper function takes a markup record with the fields `url` and `file-format`,
    and downloads it according to its file type.
    """
    print('\nDownloading from record!\n')
    print(markupRecord)
    numRecords = markupRecord.shape[0]
    form = markupRecord['file-format'][0]
    url = markupRecord['url'][0]
    print('form: ', form)
    print('url: ', url)
    if form == 'git':
        gitDownload(url, destination)
    if form == 'zip':
        zipDownload(url, destination)
    if form == 'tar.gz':
        tarDownload(url, destination)

def gitDownload(url, destination):
    print('Now git cloning from URL %s to %s' % (url, destination))
    print(sh.cd(destination))
    print(sh.pwd())
    for line in sh.git.clone(url, '--progress', _err_to_out=True, _iter=True):
        print(line)
    return

def zipDownload(url, destination):
    print('Now downloading zip from URL %s to %s' % (url, destination))
    print(sh.cd(destination))
    sh.wget(url)
    for line in sh.wget(url, _err_to_out=True, _iter=True):
        print(line)
    return

def tarDownload(url, destination):
    print('Now downloading tarball from URL %s to %s' % (url, destination))
    return

if __name__ == '__main__':
    cli()
