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
        for column in range(maze_size):
            snapshot = take_cell_snapshot(image, row, column, maze_size)
            north = snapshot[:cell_quarter, cell_quarter:-cell_quarter]
            west = snapshot[cell_quarter:-cell_quarter, :cell_quarter]
            walls.extend([north.mean(), west.mean()])

    data = whiten(walls)
    for _ in range(100):
        try:
            codebook, labels = kmeans2(data=data, k=2, missing='raise')
            break
        except ClusterError:
            continue
    else:
        raise RuntimeError('Could not find centroids for the cluster!')
    return labels


def labels_to_text(labels, maze_size):
    wall = labels[0]
    output = ''
    for i in range(maze_size):
        for j in range(maze_size):
            if labels[::2][i * maze_size + j] == wall:
                output += 'o---'
            else:
                output += 'o   '
        output += 'o\n'
        for j in range(maze_size):
            if labels[1::2][i * maze_size + j] == wall:
                output += '|   '
            else:
                output += '    '
        output += '|\n'
    output += 'o---' * maze_size + 'o\n'
    return output


def convert(image_path, maze_size, output_path):
    image = imread(image_path, as_gray=True)
    labels = image_to_labels(image, maze_size=maze_size)
    text = labels_to_text(labels, maze_size=maze_size)
    output_path.write_text(text)
