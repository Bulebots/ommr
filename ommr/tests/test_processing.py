from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest

from ommr.processing import convert


files_path = Path(__file__).resolve().parent / 'files'
maze_images = list(files_path.glob('*.png'))
maze_images = pytest.mark.parametrize('image', maze_images,
                                      ids=[str(x.relative_to(files_path))
                                           for x in maze_images])


@maze_images
def test_convert(image):
    """
    Test `convert()` function.
    """
    maze_size = int(image.name.split('-')[0].split('x')[0])
    with NamedTemporaryFile() as tmpfile:
        tmpfile = Path(tmpfile.name)
        convert(image, maze_size=maze_size, output_path=tmpfile)
        result = tmpfile.read_text()
    assert result == image.with_suffix('.txt').read_text()
