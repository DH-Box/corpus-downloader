import click
import yaml
import pandas
from tabulate import tabulate

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
    """Corpus is a command line tool that downloads textual corpora. 

    This tool was originally created for use in the Digital Humanities
    toolbox called DHBox. 
    """
    # Create a config object and remember it as as the context object.  From
    # this point onwards other commands can refer to it by using the
    # @pass_obj decorator.
    ctx.obj = Config()
    
@cli.command()
@click.option('--centuries', help='Comma-separated list of centuries to display, e.g. 16th,17th.')
@click.pass_obj
def list(ctx, centuries):
    """Lists corpora available for download."""
    click.echo('Listing!')
    click.echo(ctx.downloadTo)
    corpuslist = readCorpusList()

    if centuries: 
        centuries = centuries.split(',')
        print(centuries)



    fields = ['shortname', 'title', 'centuries', 'categories']
    showCorpusList(corpuslist, fields, centuries)
    
@click.pass_obj
def readCorpusList(ctx): 
    try: 
        corpusList = open(ctx.listFilename).read()
    except: 
            raise click.ClickException("Couldn't read the corpus list from %" % ctx.listFilename)
    try: 
        corpusListDict = yaml.safe_load(corpusList)
    except: 
            raise click.ClickException("Couldn't parse the corpus list from %.\
                    Is it in the right format?" % ctx.listFilename)
    return corpusListDict

def showCorpusList(corpuslist, fields, centuries=None):
    df = pandas.DataFrame(corpuslist)
    table = df[fields]
    pandas.set_option('display.width', None) # set that as the max width in Pandas

    if centuries is not None: 
        centuries = ('|').join(centuries) # Pandas format for OR statements is like "16th|17th"
        table = table[table['centuries'].str.contains(centuries, na=False)]
    print(table)

@cli.command()
@click.argument('src')
@click.argument('dest', required=False)
def download(src, dest):
    """Downloads a corpus.

    This will clone the repository at SRC into the folder DEST.  If DEST
    is not provided this will automatically use the default download
    location.
    """
    if dest is None:
        dest = config.download
    click.echo('Downloading corpus %s to %s' % (src, os.path.abspath(dest)))
    repo.home = dest

if __name__ == '__main__':
    cli()
