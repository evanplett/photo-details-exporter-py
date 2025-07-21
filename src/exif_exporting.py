import csv
from os.path import abspath
from pathlib import Path
from typing import Any, Dict, List, Set
from exif import Image


def get_files_in_directory(directory: Path, extensions: List[str]) -> List[Path]:
    ''' Gets a list of files in a directory '''
    directory = abspath(directory)

    print(f'#### Reading files from "{directory}" with extension(s) "{extensions}"')

    return [
        p.resolve()
        for p in Path(directory).glob("**/*")
        if p.suffix in extensions
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

def get_exif_tags_from_file(file: Path) -> Set[str]:
    ''' Gets the EXIF tags present in an image '''
    with open(file, 'rb') as image_file:
        try:
            image = Image(image_file)
            return set(image.get_all().keys()) if image.has_exif else set()
        except Exception:
            return set()


def export_exif_data_from_files_in_directory(directory: Path, extensions: List[str], tags: List[str], output_file: Path):
    ''' Exports the EXIF data from all files in a directory that match extensions '''

    fields = ["File"] + tags
    rows = [extract_exif_data_from_file(file, tags) for file in get_files_in_directory(directory, extensions)]

    output_file = output_file.absolute()
    print (f"Writing output to '{output_file}'")

    with open(output_file, 'w', encoding="UTF-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(fields)
        csv_writer.writerows(rows)
