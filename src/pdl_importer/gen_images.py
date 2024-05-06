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

def generate_images_rdf(source_file:str, output_file:str) -> None:
    source_data:Path = Path(source_file)
    out_file = Path(output_file)

    if not source_data.is_file():
        print(f"source file {source_file} not a file")
        sys.exit(1)

    importer:Importer = Importer()
    importer.import_images(source_data)
    importer.export_images(out_file)


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="process image data into rdf")
    parser.add_argument(
        "--version",
        action="version",
        version=f"pdl_importer {__version__}",
    )
    parser.add_argument(dest="source", help="source json file")
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
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.info("Starting rdf generation...")
    generate_images_rdf(args.source, args.outfile)
    _logger.info("Generation complete")


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
