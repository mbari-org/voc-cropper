# CHANGELOG

## v0.3.6 (2024-07-22)

### Performance

* perf: only open images if valid annotation found for speed-up ([`d219ab8`](https://github.com/mbari-org/voc-cropper/commit/d219ab8b3240dc72b3054a619cc506efc8ae949a))

### Unknown

* Update README.md

added raw link for better support in docker ([`609a47e`](https://github.com/mbari-org/voc-cropper/commit/609a47e3fbbff317723d8f5d82a26edd89f6e21d))

## v0.3.5 (2024-06-26)

### Fix

* fix: added version extract from tag ([`097b7db`](https://github.com/mbari-org/voc-cropper/commit/097b7db2c4662f1fc9b9f2cd7ffda76356b3525c))

## v0.3.4 (2024-06-26)

### Fix

* fix: added prerelease ([`27d1dcb`](https://github.com/mbari-org/voc-cropper/commit/27d1dcb640f3a0a60469c75e2145797558a8f68e))

## v0.3.3 (2024-06-26)

### Fix

* fix: correct release boolean? ([`4318d9e`](https://github.com/mbari-org/voc-cropper/commit/4318d9e0795332b30f26a3e140783dd50416908a))

## v0.3.2 (2024-06-26)

### Fix

* fix: correct release boolean ([`400b5e1`](https://github.com/mbari-org/voc-cropper/commit/400b5e152bd321fb2b80d9ecd56245bff389466a))

## v0.3.1 (2024-06-26)

### Fix

* fix: do not override the dst_file for resize and revert release change which fails ([`1ffe03f`](https://github.com/mbari-org/voc-cropper/commit/1ffe03f5c71565d41621fb53cb16ac9c15061942))

## v0.3.0 (2024-06-25)

### Feature

* feat: switch to id to be more generic ([`24bd8de`](https://github.com/mbari-org/voc-cropper/commit/24bd8dec4c100ed7ec2acc74f4b9155c9073a5fa))

## v0.2.0 (2024-06-25)

### Feature

* feat: add support for uuid in xml and add machine friendly names as an option ([`295f17b`](https://github.com/mbari-org/voc-cropper/commit/295f17beb70d7b0d4ff480fb647b7cefad9c2a61))

## v0.1.1 (2024-06-25)

### Build

* build: add sys path ([`13461fa`](https://github.com/mbari-org/voc-cropper/commit/13461fa6d789538f7d16471da9c68640f0a123f9))

### Fix

* fix: correct source structure ([`9cbc2e2`](https://github.com/mbari-org/voc-cropper/commit/9cbc2e23d70e3d0c218dd8ac51fd0676df133e52))

## v0.1.0 (2024-06-25)

### Build

* build: added version to command ([`682c6ba`](https://github.com/mbari-org/voc-cropper/commit/682c6ba7828bc91be3968f088c882e8d78a158fc))

* build: added QEMU to to build a multi-platform image ([`e1adaf2`](https://github.com/mbari-org/voc-cropper/commit/e1adaf23d004fb80a2dc46438dcef22cf00bc81e))

* build: removed unused dependencies from conda build for dev and upgraded open cv library ([`a5235cc`](https://github.com/mbari-org/voc-cropper/commit/a5235ccc2a264d13630c0d1a2629b0360c1414f2))

* build: added linux/amd64,linux/arm64 to the list of Docker images ([`d3c5de5`](https://github.com/mbari-org/voc-cropper/commit/d3c5de5b730787491e5d6fd4a85f5ef71de58763))

* build: switch platforms to M1 ([`81368cb`](https://github.com/mbari-org/voc-cropper/commit/81368cb51844c105fc6bf054e1884d859943e684))

* build: simplified release to latest tag sans release tags ([`2b381b3`](https://github.com/mbari-org/voc-cropper/commit/2b381b33f09ecbc970d0d2175d7ae4c08611803a))

* build: switch to tf-models-official ([`37e641b`](https://github.com/mbari-org/voc-cropper/commit/37e641b7685cc16007eb6bae670b1c4e2d3e1c05))

### Documentation

* docs: added resizing information ([`f95bb18`](https://github.com/mbari-org/voc-cropper/commit/f95bb18d5318add768a7559fd1213247b29cd3fa))

* docs: added missing resize option ([`4d6bfd6`](https://github.com/mbari-org/voc-cropper/commit/4d6bfd6b2383bb11435d35b945dc97987eeaf0b5))

* docs: updated docs ([`97bacd9`](https://github.com/mbari-org/voc-cropper/commit/97bacd924b84ec8e59d3ac2c98e791723c0b614c))

* docs: correct argument name ([`1e19c60`](https://github.com/mbari-org/voc-cropper/commit/1e19c6054b7c6996522bfce853ef03e8c9329fde))

* docs(readme.md): removed html and added MBARI link ([`f2e9c90`](https://github.com/mbari-org/voc-cropper/commit/f2e9c90120a19d59e4fb1543e8196d6b15829d51))

* docs: changes to reflect new repo name

updated flow image and associated doc to reflect new repo/docker image name ([`08fded7`](https://github.com/mbari-org/voc-cropper/commit/08fded7d63731c75c41643e77089f561a0d5bb32))

* docs: reformatted image to remove black space ([`4600764`](https://github.com/mbari-org/voc-cropper/commit/46007640dc4298d3c3a8b81ba044cfa65878a92f))

### Feature

* feat: added better square cropping algorithm ([`ef42a69`](https://github.com/mbari-org/voc-cropper/commit/ef42a699c73631bbc0f412963d828662063c4106))

* feat: merged multiproc, added logging, and removed unused features ([`3c80c21`](https://github.com/mbari-org/voc-cropper/commit/3c80c21581db170b56654541584565f291c4a55d))

* feat: slimmed docker image and replaced docker id with user id ([`d5466d6`](https://github.com/mbari-org/voc-cropper/commit/d5466d6c51220d233d53a0563f846ce309b18047))

* feat: initial check-in ([`ea22ee2`](https://github.com/mbari-org/voc-cropper/commit/ea22ee28837b28d040509020127c8e217035d910))

### Fix

* fix: write log to writable dir and add progressbar2 ([`6349145`](https://github.com/mbari-org/voc-cropper/commit/63491459c20046bcf4551dcc6307f1c9d945f726))

* fix: added missing progressbar dependency ([`0c77cf1`](https://github.com/mbari-org/voc-cropper/commit/0c77cf1c72c54ec557ffc11188966a3cf2449b5b))

* fix: hack to support drone image JPG encoding ([`6878e7c`](https://github.com/mbari-org/voc-cropper/commit/6878e7ce12f00089b3084743c96183c1fb1eab75))

* fix: invalid literal for int with base 10 error ([`3b8e386`](https://github.com/mbari-org/voc-cropper/commit/3b8e3869e8079e410f02b7dbd3255be760dfcdd5))

* fix: updated tensorflow build ([`4a9c718`](https://github.com/mbari-org/voc-cropper/commit/4a9c7180e063d6975c33a2a3b082b18cd83e4ba1))

### Performance

* perf: remove unneeded scipy dependency ([`f97ad33`](https://github.com/mbari-org/voc-cropper/commit/f97ad3377281cfa1d284168654cd0bf99f7e7d13))

* perf: use xmltodict to reduce size of image/dependencies ([`c132988`](https://github.com/mbari-org/voc-cropper/commit/c132988ace2bbfb30fbb34c980785c669e63e4b9))

* perf: bumped to newer python and add docker release ([`1915e36`](https://github.com/mbari-org/voc-cropper/commit/1915e36884bc66f835c77eb8caff056a664dd3c1))

### Unknown

* minor markdown related edits ([`c5a0fa2`](https://github.com/mbari-org/voc-cropper/commit/c5a0fa2c5afe5786b01bb56ccbeb34ba137fc9bc))
