import click
import os
import subprocess
import py

DIR = os.path.dirname(os.path.realpath(__file__))


@click.group()
def main():
    """The main routine"""


@main.command()
@click.option('-p', '--port', default=9999, help='Port [9999]')
def local(port):
    """Run UWSGi in local mode"""
    bashCommand = (
        "uwsgi"
        " --http :%s"
        " --wsgi-file %s/restapi.py"
        " --callable api"
        % (port, DIR)
    )
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


@main.command()
@click.option('-p', '--port', default=8080, help='Port [8080]')
def run(port):
    """Run UWSGi in production mode"""
    bashCommand = (
        "uwsgi"
        " --socket localhost:%s"
        " --wsgi-file %s/restapi.py"
        " --callable api"
        % (port, DIR)
    )
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

main(prog_name='catcher')

if __name__ == "__main__":
    print("Run \"catcher --help\"")
