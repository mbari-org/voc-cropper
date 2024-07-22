[![MBARI](https://www.mbari.org/wp-content/uploads/2014/11/logo-mbari-3b.png)](http://www.mbari.org)

[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)
![Supported Platforms](https://img.shields.io/badge/Supported%20Platforms-Windows%20%7C%20macOS%20%7C%20Linux-green)
![license-GPL](https://img.shields.io/badge/license-GPL-blue)

# About

*voc-imagecropper* is a simple utility to crop from PNG or JPEG images bounding box annotations in PASCAL VOC formatted annotations.
This is used to crop (and optionally resize) images from full frames for classification testing.
    
---
![](https://raw.githubusercontent.com/mbari-org/voc-cropper/main/img/flow.jpg)
---

## *Arguments* 

  * run as you:  `-u $(id -u):$(id -g)`
  * remove after running: `--rm`
  * run interactively: `-it`
  * `--resize` the cropped image to the specified size, e.g. `--resize 128x128` crop then resizes to 128x128
  * `-d` root directory to the raw data
  * `-o` path to output image crops to
  * `--minsize minimum` size pixel width or height dimension - useful to remove images too small for classification
  * `--machine_friednly` output class names with underscores instead of spaces, or special characters, e.g. dots, e.g. `sp_A` instead of `sp. A`
  * (optional) `--labels` list of space separated labels to load - defaults to everything. 
  * (optional) `--image_dir` path where raw images associated with the annotations are located - overrides those defined
  in the PASCAL formatted annotations

## Note

An exception to the standard PASCAL VOC format is that the `uuid` is used.  If that exists in the annotation, it is used to name the prefix of the output file.  
If not, the filename is used with an appended integer prefix.  This is to ensure unique filenames for the cropped images.

## Build

You can skip this step if you are using the pre-built docker image.

```bash
docker build -t mbari/voc-imagecropper .
```
## *Run example*

```bash
docker run -it \
--rm -u $(id -u):$(id -g) \
-v $PWD/data:/data mbari/voc-imagecropper \
-d /data/annotations \
--image_dir /data/imgs \
-o /data/out
```

Should see output similar to:
```bash
2023-07-17 22:06:09,885 INFO Searching in data/annotations for .xml files
2023-07-17 22:06:09,886 INFO Found 1 files
2023-07-17 22:06:09,886 INFO Using 1 processes to convert 1 annotations ...
2023-07-17 22:06:10,341 INFO Calculating mean and std ...
2023-07-17 22:06:10,341 INFO Computing statistics for data
Computing statistics for data : 100% (1 of 1) || Elapsed Time: 0:00:00 Time:  0:00:00
2023-07-17 22:06:10,491 INFO Writing data/stats.txt
2023-07-17 22:06:10,492 INFO Number of concepts: 1
2023-07-17 22:06:10,492 INFO Number of frames: 1
2023-07-17 22:06:10,492 INFO Mean: [0.33466873 0.40399225 0.39004853]
2023-07-17 22:06:10,492 INFO Std: [0. 0. 0.]
2023-07-17 22:06:10,492 INFO Writing data/labels.txt
```
