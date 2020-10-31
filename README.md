[![MBARI](https://www.mbari.org/wp-content/uploads/2014/11/logo-mbari-3b.png)](http://www.mbari.org)

[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)
![Supported Platforms](https://img.shields.io/badge/Supported%20Platforms-Windows%20%7C%20macOS%20%7C%20Linux-green)
![license-GPL](https://img.shields.io/badge/license-GPL-blue)

# About

* deepsea-imagecropper * is a simple utility to crop from PNG or JPEG images bounding box annotations in PASCAL formatted annotations.
This is used to crop images for classification testing.
    
![ Image link ](/img/flow.jpg)

## *Arguments* 

  * run as you -u $(id -u):$(id -g)
  * remove after running --rm
  * run interactively -it
  * -d root directory to the raw data
  * -o path to output image crops to
  * --minsize minimum size pixel width or height dimension - useful to remove images too small for classification
  * (optional) --labels list of space separated labels to load - defaults to everything. 
  * (optional) --image_path path where raw images associated with the annotations are located - overrides those defined
  in the PASCAL formatted annotations

## Build

```bash
docker build -t mbari/deepsea-imagecropper .
```
## *Run example*

```bash
docker run -it \
--rm -u $(id -u):$(id -g) \
-v $PWD/data:/data mbari/deepsea-imagecropper \
-d /data/annotations \
--image_dir /data/imgs \
-o /data/out
```

Should see output
```bash
Searching in /data/annotations
Found /data/annotations/IMG_5137.xml
Cropping left 2448.0 upper 1389.0 right 2648.0 lower 1589.0
Done. Found 1 examples.
Image mean [91.26420774 93.76789747 77.57847996] normalized [0.35789885 0.36771724 0.30422933]
Total PENIAGONE_VITREA = 1
```
