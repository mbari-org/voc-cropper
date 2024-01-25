#!/usr/bin/env python

__author__ = "Danelle Cline"
__copyright__ = "Copyright 2020, MBARI"
__credits__ = ["MBARI"]
__license__ = "GPL"
__maintainer__ = "Danelle Cline"
__email__ = "dcline at mbari.org"
__doc__ = '''

Crops images from bounding box annotations in PASCAL records

@author: __author__
@status: __status__
@license: __license__
'''

from PIL import JpegImagePlugin
JpegImagePlugin._getmp = lambda: None
import io
from datetime import datetime as dt
import glob
import os
import numpy as np
import logging
import sys
import cv2

from pathlib import Path
import json
import multiprocessing
import numpy as np
import codecs
import progressbar
from PIL import Image, ImageStat

assert (callable(progressbar.progressbar)), "Using wrong progressbar module, install 'progressbar2' instead."

import xmltodict
from PIL import Image


LOGGER_NAME = "VOCCROPPER"
DEBUG = True

def process_command_line():
    """
    Process command line
    :return: args object
    """

    import argparse
    from argparse import RawTextHelpFormatter

    examples = 'Examples:' + '\n\n'
    examples += 'Create record for xml files in /data:\n'
    examples += '{} --data_dir /data --image_dir /data/imgs --output_path /data/crops '.format(
        sys.argv[0])
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter,
                                     description='Creates crops from PASCAL files annotated data',
                                     epilog=examples)
    parser.add_argument('-d', '--data_dir', action='store', help='Root directory to raw dataset', required=True)
    parser.add_argument('--override_size', help='Overrides raw image size in data set and adjust crops to this scale.',
                        required=False, type=str)
    parser.add_argument('--image_dir', action='store', help='String specifying subdirectory within the PASCAL '
                                                            'dataset directory holding the actual image data',
                        default=None, required=False)
    parser.add_argument('--minsize', type=int, required=False, default=0,
                        help="minimum size pixel width or height dimension. "
                             "Useful to remove images too small for classification")
    parser.add_argument('--resize', help='Resize images to wxh', required=False, type=str)
    parser.add_argument('-o', '--output_path', action='store', help='Path to store image crops', required=True)
    parser.add_argument('--labels', action='store',
                        help='List of space separated labels to crop. Defaults to everything', nargs='*',
                        required=False)

    args = parser.parse_args()
    return args


def is_valid_xml(xml_filename):
    """
    Simple check if xml file container dictionary starting with annotation root
    :param xml_filename:
    :return:
    """
    try:
        with open(xml_filename, 'rb') as fid:
            xml_str = fid.read()
        xmltodict.parse(xml_str)
        return True
    except Exception as ex:
        return False

def file_search(path, extensions):
    for ext in extensions:
        f = path + ext
        if os.path.exists(f):
            return f
    return None


def gen_statistics(data_dir: str, stats_file: str, labels_file: str):
    """
    This computes statistics for a collection of images and stores them in a json file.
    :param data_dir: Absolute path to the directory with .png files
    :param stats_file: Absolute path to the filename to store the statistics
    :param labels_file: Absolute path to the filename to store the labels
    :return: statistics dictionary
    """

    logger = logging.getLogger(LOGGER_NAME)
    logger.info(f'Computing statistics for {data_dir}')

    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    sum_concepts = {}
    means = []
    stds = []
    mean = np.array([])
    std = np.array([])

    for g in progressbar.progressbar(sorted(glob.glob(f'{data_dir}/**/*.jpg')),
                                     prefix=f'Computing statistics for {data_dir} : '):
        g_path = Path(g)
        c = g_path.parent.name
        img = Image.open(g_path.as_posix())
        stat = ImageStat.Stat(img)
        mean = stat.mean
        std = stat.stddev
        means.append(mean)
        stds.append(std)

        if c not in sum_concepts.keys():
            sum_concepts[c] = 1
        else:
            sum_concepts[c] += 1

    if len(means) > 0:
        mean = np.mean(means, axis=(0)) / 255.
        std = np.std(stds, axis=(0)) / 255.

    logger.info(f'Writing {stats_file}')
    json.dump({'total_concepts': sum_concepts, 'mean': mean.tolist(), 'std': std.tolist()},
              codecs.open(stats_file, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)

    # Print out the statistics
    logger.info(f'Number of concepts: {len(sum_concepts)}')
    logger.info(f'Number of frames: {sum(sum_concepts.values())}')
    logger.info(f'Mean: {mean}')
    logger.info(f'Std: {std}')

    # Stores all unique labels to the labels_file, one per line
    logger.info(f'Writing {labels_file}')
    with open(labels_file, 'w') as f:
        for key in sum_concepts.keys():
            f.write("%s\n" % key)


def dict_to_images(xml_file: str,
                   output_dir,
                   labels,
                   minsize,
                   image_dir=None,
                   resize=None):
    """
    Convert XML derived dict to images
    :param output_dir: output directory to store cropped images to
    :param xml_in:  xml with metadata
    :param data: data dictionary
    :param labels: list of labels to include in the crops
    :param minsize: minimum size in pixels for width/height for image crops
    :param image_dir: alternative images directory with raw images
    :param resize: size to rescale crops
    :return: dictionary of total crops per label
    :raises:  ValueError: if the image pointed to by data['filename'] is not a valid JPG or PNG
    """

    logger = logging.getLogger(LOGGER_NAME)

    try:
        with open(xml_file, 'rb') as fid:
            xml_str = fid.read()
        xml_in = xmltodict.parse(xml_str)
        data = xml_in['annotation']
        root = os.path.basename(xml_file).split('.')[0]

        if image_dir:
            data['folder'] = image_dir
            img_path = file_search(os.path.join(image_dir, root), ('.jpeg', '.jpg', '.JPG', '.JPEG', '.PNG', '.png'))
            if img_path is None:
                logging.error(f'Cannot find image associated with {xml_file}')
                return

            logger.info(f'found {img_path}')
            data['filename'] = img_path

        with open(img_path, 'rb') as fid:
            encoded_img = fid.read()
        encoded_img_io = io.BytesIO(encoded_img)
        rgb_image = Image.open(encoded_img_io)
        if rgb_image.format != 'PNG' and rgb_image.format != 'JPEG':
            logger.error('Invalid image format ' + rgb_image.format)
            raise ValueError('Invalid image format ' + rgb_image.format)

        img = cv2.imread(img_path)
        object_ = data['object']
        # object_ will be a list when multiple <object> entries present, otherwise a dict:
        objs = object_ if type(object_) is list else [object_]
        for i, obj in enumerate(objs):
            # Convert a machine friendly name, replacing sp. and white spaces with underscores
            name = obj['name'].replace(' ', '_')
            name = name.replace('sp.', 'sp_')
            if labels and (name not in labels or obj['name'] not in labels):
                logger.warn('{0} not in {1} so excluding from record'.format(name, labels))
                continue
            if 'SALIENCY' in name:
                logger.info('skipping {}'.format(name))
                continue

            class_dir = '{}/{}'.format(output_dir, name)
            if not os.path.exists(class_dir):
                logger.info('Creating directory {}'.format(class_dir))
                os.mkdir(class_dir)

            xmin = int(float(obj['bndbox']['xmin']))
            ymin = int(float(obj['bndbox']['ymin']))
            xmax = int(float(obj['bndbox']['xmax']))
            ymax = int(float(obj['bndbox']['ymax']))

            left = int(xmin)
            right = int(xmax)
            upper = int(ymin)
            lower = int(ymax)

            # if the resize is a square, then we need to pad the image to make it square
            resize_width, resize_height = resize if resize else (0, 0)
            if resize and resize_width == resize_height:
                # Use padding if resizing to a square
                width = left - right
                height = upper - lower
                shorter_side = min(height, width)
                longer_side = max(height, width)
                delta = abs(longer_side - shorter_side)

                # Divide the difference by 2 to determine how much padding is needed on each side
                padding = delta // 2

                # Add the padding to the shorter side of the image
                if width == shorter_side:
                    left -= padding
                    right += padding
                else:
                    upper -= padding
                    lower += padding

            # only keep crops larger than minsize pixels in at least one dimension
            if abs(left - right) > minsize or abs(upper - lower) > minsize:
                logger.info('Cropping left {} right {} upper {} lower {}'.format(left, right, upper, lower))
                img2 = img[upper:lower, left:right]
                if resize:
                    img2 = cv2.resize(img2, dsize=resize, interpolation=cv2.INTER_CUBIC)
                dst_file = '{}/{}/{}_{}.jpg'.format(output_dir, name, root, i)
                cv2.imwrite(dst_file, img2, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            else:
                logger.info('Too small to convert width {} height {}'.format(abs(left - right), abs(upper - lower)))

    except Exception as ex:
        logging.exception(ex)


def main():
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

    # default log file date to today
    now = dt.utcnow()

    # log to file
    # Log to the /tmp directory if we don't have write access to the current directory
    if not os.access(os.getcwd(), os.W_OK):
        logger.info(f'No write access to {os.getcwd()} so logging to /tmp')
        log_filename = f"/tmp/{LOGGER_NAME}_{dt.utcnow():%Y%m%d}.log"
    else:
        log_filename = f"{LOGGER_NAME}_{dt.utcnow():%Y%m%d}.log"
    handler = logging.FileHandler(log_filename, mode="w")
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)

    logger.info(f"Logging to {log_filename}")

    # log to console
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG if DEBUG else logging.INFO)
    logger.addHandler(handler)

    args = process_command_line()

    output_dir = args.output_path

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    annotations = []
    logger.info('Searching in {} for .xml files'.format(args.data_dir))
    for xml_in in glob.glob(args.data_dir + '/*.xml'):
        if is_valid_xml(xml_in):
            annotations.append(xml_in)

    logger.info('Found {} files'.format(len(annotations)))
    filter_labels = None

    if args.labels:
        filter_labels = args.labels

    if args.resize:
        width = int(args.resize.split('x')[0])
        height = int(args.resize.split('x')[1])
        resize = (width, height)
    else:
        resize = None

    # Use a pool of processes to speed up
    num_processes = min(multiprocessing.cpu_count(), len(annotations))
    num_processes = max(1, num_processes)
    logger.info(f'Using {num_processes} processes to convert {len(annotations)} annotations ...')
    with multiprocessing.Pool(num_processes) as pool:
        args = [(e, output_dir, filter_labels, args.minsize, args.image_dir, resize) for e  in annotations]
        pool.starmap(dict_to_images, args)

    logger.info(f'Calculating mean and std ...')
    stats_file = os.path.join(output_dir, 'stats.txt')
    labels_file = os.path.join(output_dir, 'labels.txt')
    gen_statistics(output_dir, stats_file, labels_file)


if __name__ == '__main__':
    main()
