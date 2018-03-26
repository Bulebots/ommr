from pathlib import Path
from tempfile import NamedTemporaryFile

import numpy
import pytest

from ommr.processing import convert
from ommr.processing import image_to_labels


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


def test_image_to_labels_blank():
    """
    Test `image_to_labels()` function with a blank image as input.

    It should be impossible to calculate the centroids, so an exception must
    be raised.
    """
    blank = numpy.ones((200, 200)) - 0.1
    with pytest.raises(RuntimeError):
        image_to_labels(image=blank, maze_size=16)
