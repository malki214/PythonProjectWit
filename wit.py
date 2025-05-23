
import click
import os
from Repository import Repository


@click.group()
def cli():
    """ Wit Version Control CLI """
    pass

# יצירת מופע של המאגר הנוכחי שעליו יופעלו הפונקציות
current_repository = Repository(os.getcwd())

@click.command()
def init():
    click.echo(current_repository.init())


@click.command()
@click.argument('file_name')
def add(file_name):
    click.echo(current_repository.add(file_name))


@click.command()
@click.argument('version_name')
def commit (version_name):
    click.echo(current_repository.commit(version_name))

@click.command()
def log():
    click.echo(current_repository.log())

@click.command()
def status():
    click.echo(current_repository.status())

@click.command()
@click.argument('id')
@click.argument('file_name',required = False)
def checkout (id, file_name):
    click.echo(current_repository.checkout(id, file_name))

# הוספת הפקודות לקבוצת ה-CLI
cli.add_command(init)
cli.add_command(add)
cli.add_command(commit)
cli.add_command(log)
cli.add_command(status)
cli.add_command(checkout)


if __name__ == '__main__':
    cli()

