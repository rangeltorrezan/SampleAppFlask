__author__ = 'wellington.nukamoto'

import time
import pytest
import logging
import pytest_cov
from paver.easy import *
from paver.path import path
from paver.setuputils import setup
from watchdog.events import PatternMatchingEventHandler
from pylint.lint import Run
from pylint.reporters.text import TextReporter
from io import StringIO
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

DOMAIN_PACKAGE = 'domain'
CONTROLLER_PACKAGE = 'controller'
TEST_PACKAGE_DOMAIN = 'controller/test'
TEST_PACKAGE_CONTROLLER = 'domain/test'
PROJECT_ROOT = path(__file__).abspath().dirname()
#SOURCE_ROOT = PROJECT_ROOT / SOURCE_PACKAGE
TEST_ROOT = PROJECT_ROOT
REPORT_ROOT = PROJECT_ROOT / 'report'
REPORT_PYLINT = REPORT_ROOT / 'pylint.txt'
REPORT_RADON_CC = REPORT_ROOT / 'radon_cc.txt'
REPORT_RADON_RAW = REPORT_ROOT / 'radon_raw.txt'
REPORT_RADON_MI = REPORT_ROOT / 'radon_mi.txt'
REPORT_COVERAGE = REPORT_ROOT / 'coverage.xml'

setup(
    name = 'changeit',
    packages = [DOMAIN_PACKAGE, CONTROLLER_PACKAGE],
    version = '0.0.1',
    url = 'http://www.nexxera.com/',
    author = 'wellington.nukamoto',
    author_email = 'wellington.nukamoto@nexxera.com',
    test_suite = [TEST_PACKAGE_DOMAIN,TEST_PACKAGE_CONTROLLER]
)

@task
def clear():
    path(REPORT_ROOT).rmtree()

@task
@consume_args
def pylint(args):
    """
    :param args: report para salvar em arquivo
    :return:
    """
    my_output = StringIO()
    configuration_pylint = [DOMAIN_PACKAGE, CONTROLLER_PACKAGE, '--rcfile=.pylintrc']
    if len(args)> 0 and args[0] == 'report':
        Run(configuration_pylint, reporter = TextReporter(output = my_output), exit = False)
        output_str = my_output.getvalue()
        path(REPORT_ROOT).mkdir()
        path(REPORT_PYLINT).write_text(output_str, linesep = '\r\n', append = False)
    else:
        configuration_pylint += ['-r','n']
        Run(configuration_pylint, exit = False)

@task
@consume_args
def coverage(args):
    """
    :param args: report para salvar em arquivo
    :return:
    """
    configuration_coverage = [
        '--doctest-modules', '--cov', DOMAIN_PACKAGE, '--cov', CONTROLLER_PACKAGE,
        '--cov-report', 'term-missing',
        TEST_ROOT
    ]
    if len(args) > 0 and args[0] == 'report':
        configuration_coverage += ['--junitxml', REPORT_COVERAGE]
    pytest.main(configuration_coverage)

@task
@consume_args
def radon_cc(args):
    """
    1 - 5   A   low - simple block
    6 - 10  B   low - well structured and stable block
    11 - 20 C   moderate - slightly complex block
    21 - 30 D   more than moderate - more complex block
    31 - 40 E   high - complex block, alarming
    41+ F   very high - error-prone, unstable block 
    :param args: report para salvar em arquivo
    :return:
    """
    if len(args) > 0 and args[0] == 'report':
        sh('radon cc -na %s/* %s/* > %s' % (DOMAIN_PACKAGE, CONTROLLER_PACKAGE, REPORT_RADON_CC))
    else:
        sh('radon cc -nb %s/* %s/*' % (DOMAIN_PACKAGE, CONTROLLER_PACKAGE))

@task
@consume_args
def radon_raw(args):
    """
    :param args: report para salvar em arquivo
    :return:
    """
    if len(args) > 0 and args[0] == 'report':
        sh('radon raw -s %s/* %s/* > %s' % (DOMAIN_PACKAGE, CONTROLLER_PACKAGE, REPORT_RADON_RAW))

@task
@consume_args
def radon_mi(args):
    """
    :param args: report para salvar em arquivo
    :return:
    """
    if len(args) > 0 and args[0] == 'report':
        sh('radon mi -s %s/* %s/* > %s' % (DOMAIN_PACKAGE, CONTROLLER_PACKAGE, REPORT_RADON_MI))

@task
@consume_args
@needs(['clear'])
def build(args):
    """
    :param args:
    :return:
    """
    sh('clear')
    call_task('coverage', args)
    call_task('pylint', args)
    call_task('radon_cc', args)
    call_task('radon_raw', args)
    call_task('radon_mi', args)

@task
def dev():
    executar_app()

@task
def prod():
    executar_app('export PYTHONPATH=./controller:./config:./domain; gunicorn -w 4 --bind 0.0.0.0:8000 wsgi:app')


def executar_app(chamada = 'python wsgi.py'):
    """
    :param args:
    :return:
    """
    observer = Observer()
    observer.schedule(DotPyChangesEventHandler(), PROJECT_ROOT, recursive = False)
    observer.start()
    sh(chamada)

class DotPyChangesEventHandler(PatternMatchingEventHandler):
    patterns = ['*.py']
    def on_modified(self, event):
        call_task('build', args = [''])
