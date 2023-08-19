import argparse
import csv
from os.path import abspath
from pathlib import Path
from typing import List
from exif import Image


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

def get_files_in_directory() -> List[Path]:
    ''' Gets a list of files in a directory '''
    directory = abspath(args.directory)

    extensions = args.extension or [[DEFAULT_EXTENSION]]
    extensions_flat = [add_period(item) for sublist in extensions for item in sublist]

    print(f'#### Reading files from "{directory}" with extension(s) "{extensions_flat}"')

    return [
        p.resolve()
        for p in Path(directory).glob("**/*")
        if p.suffix in extensions_flat
    ]

def extract_exif_data_from_file(file: Path, tags: List[str]):
    ''' Extracts the relevant EXIF data from an image '''
    with open(file, 'rb') as image_file:

        try:
            image = Image(image_file)
            if image.has_exif:
                return [file] + [getattr(image, tag, None) for tag in tags]

            return [file, "No EXIF data"]
        except Exception:
            return [file, "ERROR"]


def main():
    ''' The main logic of the application '''
    tags = args.tags or [DEFAULT_EXIF_TAGS]
    flat_tags = [item for sublist in tags for item in sublist]

    fields = ["File"] + flat_tags
    rows = [extract_exif_data_from_file(file, flat_tags) for file in get_files_in_directory()]

    output_file = Path(args.out).absolute()
    print (f"Writing output to '{output_file}'")

    with open(output_file, 'w', encoding="UTF-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(fields)
        csv_writer.writerows(rows)

if __name__ == '__main__':
    main()
