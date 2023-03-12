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
import glob
import os
import numpy as np
import logging
import sys
import cv2

import xmltodict
from PIL import Image


def process_command_line():
    '''
    Process command line
    :return: args object
    '''

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
    '''
    Simple check if xml file container dictionary starting with annotation root
    :param xml_filename:
    :return:
    '''
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

def dict_to_images(output_dir,
                   xml_in,
                   data,
                   labels,
                   minsize,
                   image_dir=None,
                   resize=None,
                   override_size=None):
    '''
    Convert XML derived dict to images
    :param output_dir: output directory to store cropped images to
    :param xml_in:  xml with metadata
    :param data: data dictionary
    :param labels: list of labels to include in the crops
    :param minsize: minimum size in pixels for width/height for image crops
    :param image_dir: alternative images directory with raw images
    :param resize: size to rescale crops
    :param override_size: size to scale annotations to instead of raw image size
    :return: dictionary of total crops per label
    :raises:  ValueError: if the image pointed to by data['filename'] is not a valid JPG or PNG
    '''
    root = os.path.basename(xml_in).split('.')[0]
    folder = data['folder']
    if image_dir:
        data['folder'] = image_dir
        img_path = file_search(os.path.join(image_dir, root), ('.jpeg', '.jpg', '.JPG', '.JPEG', '.PNG', '.png'))
        print('found ' + img_path)
        data['filename'] = img_path
    else:
        data['folder'] = xml_in.split(folder)[0]
        data['filename'] = '{}/{}.png'.format(folder, root)
        img_path = os.path.join(data['folder'], data['filename'])

    if override_size:
        wf = 960/float(data['size']['width'])
        hf = 540/float(data['size']['height'])
    else:
        wf = 1.0
        hf = 1.0

    with open(img_path, 'rb') as fid:
        encoded_img = fid.read()
    encoded_img_io = io.BytesIO(encoded_img)
    rgb_image = Image.open(encoded_img_io)
    if rgb_image.format != 'PNG' and rgb_image.format != 'JPEG':
        raise ValueError('Invalid image format ' + rgb_image.format)

    img = cv2.imread(img_path)
    my_label = {}
    object_ = data['object']
    # object_ will be a list when multiple <object> entries present, otherwise a dict:
    objs = object_ if type(object_) is list else [object_]
    for obj in objs:
        name = obj['name']
        if labels and (name not in labels or obj['name'] not in labels):
            print('{0} not in {1} so excluding from record'.format(name, labels))
            continue
        if 'SALIENCY' in name:
            print('skipping {}'.format(name))
            continue

        if name not in my_label.keys():
            my_label[name] = 0

        class_dir = '{}/{}'.format(output_dir, name)
        if not os.path.exists(class_dir):
            print('Creating directory {}'.format(class_dir))
            os.mkdir(class_dir)

        xmin = int(float(obj['bndbox']['xmin']))
        ymin = int(float(obj['bndbox']['ymin']))
        xmax = int(float(obj['bndbox']['xmax']))
        ymax = int(float(obj['bndbox']['ymax']))

        left = int(xmin*wf)
        right = int(xmax*wf)
        upper = int(ymin*hf)
        lower = int(ymax*hf)

        # only keep crops larger than minsize pixels in at least one dimension
        if abs(left - right) > minsize or abs(upper - lower) > minsize:
            print('Cropping left {} right {} upper {} lower {}'.format(left, right, upper, lower))
            img2 = img[upper:lower, left:right]
            if resize:
                img2 = cv2.resize(img2, dsize=resize, interpolation=cv2.INTER_CUBIC)
            dst_file = '{}/{}/{}_{}.jpg'.format(output_dir, name, root, int(my_label[name]))
            cv2.imwrite(dst_file, img2, [int(cv2.IMWRITE_JPEG_QUALITY),100])
            my_label[name] += 1
        else:
            print('Too small to convert width {} height {}'.format(abs(left - right), abs(upper - lower)))

    return my_label


def main():
    args = process_command_line()

    output_dir = args.output_path

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    annotations = []
    print('Searching in {}'.format(args.data_dir))
    for xml_in in glob.glob(args.data_dir + '/*.xml'):
        if is_valid_xml(xml_in):
            annotations.append(xml_in)

    print('Found {} files'.format(len(annotations)))
    means = []
    stds = []
    labels = {}
    filter_labels = None
    if args.labels:
        filter_labels = args.labels

    for idx, example in enumerate(annotations):
        if idx % 10 == 0:
            logging.info('Processing image %d of %d', idx, len(annotations))
        with open(example, 'rb') as fid:
            xml_str = fid.read()
        xml = xmltodict.parse(xml_str)
        data = xml['annotation']
        try:
            if args.resize:
                width = int(args.resize.split('x')[0])
                height = int(args.resize.split('x')[1])
                label_example = dict_to_images(output_dir, example, data, filter_labels, args.minsize, args.image_dir, (width, height), args.override_size)
            else:
                label_example = dict_to_images(output_dir, example, data, filter_labels, args.minsize, args.image_dir, None, args.override_size)

            for key, value in label_example.items():
                if key not in labels:
                    labels[key] = 0
                labels[key] += value

                img_path = os.path.join(args.image_dir, data['filename'])
                img = cv2.imread(img_path)
                means.append(np.mean(img, axis=(0, 1)))
                stds.append(np.mean(img, axis=(0, 1)))
        except Exception as ex:
            print(ex)
            continue

    mean = 0
    std = 0
    if len(means) > 0 and len(stds) > 0:
        mean = np.mean(means, axis=(0))
        std = np.mean(stds, axis=(0))
    print('Done. Found {} examples.\nImage mean {} normalized {} std {} normalized {}'.format(sum(labels.values()), mean, mean / 255, std, std / 255))
    for key, value in labels.items():
        print('Total {} = {}'.format(key, value))


if __name__ == '__main__':
    main()
