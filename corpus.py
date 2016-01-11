import click

class Config(object):
    # TODO: get config
    dest = 'data'

@click.group()
@click.version_option('0.1')
def cli():
    """Corpus is a command line tool that downloads textual corpora. 

    This tool was originally created for use in the Digital Humanities
    toolbox called DHBox. 
    """
    # Create a config object and remember it as as the context object.  From
    # this point onwards other commands can refer to it by using the
    # @pass_config decorator.

@cli.command()
def list():
    """Lists corpora available for download."""
    click.echo('Listing!')

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

