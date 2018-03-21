from pathlib import Path

from imageio import imread
from scipy.cluster.vq import ClusterError
from scipy.cluster.vq import kmeans2
from scipy.cluster.vq import whiten


def take_cell_snapshot(image, row, column, maze_size):
    x = image.shape[0] / maze_size
    y = image.shape[1] / maze_size
    return image[round(x * row):round(x * (row + 1)),
                 round(y * column):round(y * (column + 1))]


def image_to_labels(image, maze_size):
    size = (image.shape[0] + image.shape[1]) / 2
    cell_size = size / maze_size
    cell_quarter = round(cell_size / 4)
    walls = []
    for row in range(maze_size):
        north_walls = []
        west_walls = []
        for column in range(maze_size):
            snapshot = take_cell_snapshot(image, row, column, maze_size)
            north = snapshot[:cell_quarter, cell_quarter:-cell_quarter]
            west = snapshot[cell_quarter:-cell_quarter, :cell_quarter]
            north_walls.append(north.mean())
            west_walls.append(west.mean())
        # TODO: use (NORTH, WEST) tuple instead
        walls.extend(north_walls)
        walls.extend(west_walls)

    data = whiten(walls)
    for i in range(100):
        try:
            codebook, labels = kmeans2(data=data, k=2, missing='raise')
            break
        except ClusterError:
            continue
    else:
        raise RuntimeError('Could not find centroids for the cluster!')
    return labels


def labels_to_text(labels, maze_size):
    match = labels[0]
    output = ''
    for i in range(maze_size):
        for j in range(maze_size):
            if labels[2 * i * maze_size + j] == match:
                output += 'o---'
            else:
                output += 'o   '
        output += 'o\n'
        for j in range(maze_size, 2 * maze_size):
            if labels[2 * i * maze_size + j] == match:
                output += '|   '
            else:
                output += '    '
        output += '|\n'
    output += 'o---' * maze_size
    output += 'o\n'
    return output


def convert(image_path, maze_size, output_path):
    image = imread(image_path, as_gray=True)
    labels = image_to_labels(image, maze_size=maze_size)
    text = labels_to_text(labels, maze_size=maze_size)
    output_path.write_text(text)


if __name__ == '__main__':
    convert(image_path=Path('tests/files/japan2014ef.png'),
            maze_size=32,
            output_path=Path('test.txt'))
