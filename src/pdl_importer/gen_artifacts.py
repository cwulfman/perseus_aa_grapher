import argparse
import logging
import sys
from pathlib import Path
from pdl_importer import __version__
from pdl_importer.importer import Importer


__author__ = "Cliff Wulfman"
__copyright__ = "Cliff Wulfman"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from pdl_importer.skeleton import fib`,
# when using this Python module as a library.


def generate_artifacts_rdf(source_file:str, collections_file:str, output_file:str) -> None:
    source_data:Path = Path(source_file)
    collections_data = Path(collections_file)
    out_file = Path(output_file)

    if not source_data.is_file():
        print(f"source file {source_file} not a file")
        sys.exit(1)

    if not collections_data.is_file():
        print(f"collection file {collections_file} not a file")
        sys.exit(1)


    importer:Importer = Importer()
    importer.import_collections(collections_data)
    importer.import_data(source_data)
    importer.export_artifacts(out_file)



# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="process artifact data into rdf")
    parser.add_argument(
        "--version",
        action="version",
        version=f"pdl_importer {__version__}",
    )
    parser.add_argument(dest="source", help="source json file")
    parser.add_argument(dest="collections", help="collections csv file")
    parser.add_argument(dest="outfile", help="output directory")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting rdf generation...")
    generate_artifacts_rdf(args.source, args.collections, args.outfile)
    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m pdl_importer.skeleton 42
    #
    run()
