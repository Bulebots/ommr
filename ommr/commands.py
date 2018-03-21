from pathlib import Path

import click

from .processing import convert


@click.command()
@click.option('-s', '--size', type=int, default=32, help='Maze size.')
@click.option('-o', '--output', type=click.Path(), default=None,
              help='Output file name or directory.')
@click.argument('maze_image', type=click.Path())
def run(maze_image: Path, size: int=32, output: Path=None):
    """
    Optical Micromouse Maze Recognition.

    Takes an image as an input, which gets converted to the text maze file
    format.

    \b
    - If no output is specified, the same input path and file name will be
      used, only replacing the input file extension with `.txt`.
    - If the output is a directory, the same input file name will be used but
      the file will be created inside the specified output directory.
    - If the output is not a directory it will be considered the output file
      name.
    """
    maze_image = Path(maze_image)
    if output is None:
        output = maze_image.with_suffix('.txt')
    output = Path(output)
    if output.is_dir():
        output = output / maze_image.with_suffix('.txt').name
    convert(maze_image, size, output)
