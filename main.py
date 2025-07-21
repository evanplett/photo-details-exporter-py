import argparse
from pathlib import Path

from src.exif_exporting import export_exif_data_from_files_in_directory
from src.gui import create_gui


DEFAULT_EXIF_TAGS = [
    'focal_length'
]

DEFAULT_EXTENSION = "JPG"


parser = argparse.ArgumentParser(
                    prog='Photo Details Exporter',
                    description='Exports EXIF data from all files in a directory')

parser.add_argument('-d', '--directory', required=False, default=".", help="The directory to load files from. Default = '.'")
parser.add_argument('-e', '--extension', action='append', nargs="*", help="Extensions to load. Default = '.JPG'")
parser.add_argument('-o', '--out', required=False, default="exif_data.csv", help="The name of the CSV output file. Default = 'exif_data.csv'")
parser.add_argument('-t', '--tags', action='append', nargs="*", help=f"EXIF tags to export. Default = {DEFAULT_EXIF_TAGS}")
args = parser.parse_args()


def add_period(extension: str):
    ''' Adds a period to the beginning of a string if one is not present. '''
    return extension if extension.startswith('.') else f'.{extension}'


def do_cli():
    tags = args.tags or [DEFAULT_EXIF_TAGS]
    flat_tags = [item for sublist in tags for item in sublist]


    extensions = args.extension or [[DEFAULT_EXTENSION]]
    extensions_flat = [add_period(item) for sublist in extensions for item in sublist]

    export_exif_data_from_files_in_directory(Path(args.directory), extensions_flat, flat_tags, Path(args.out))

def main():
    ''' The main logic of the application '''

    create_gui()


if __name__ == '__main__':
    main()
