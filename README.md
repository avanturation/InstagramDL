# InstagramDL

> Download Instagram images, and stories simply

## Disclaimer

We do not have responsibiliy for you to download explict, harmful things.

**Use at your own risk!**

## Usage

### Download only a post
```bash
python3 . --post CPkgc--NkhZ
```

It will download contents from [here](https://www.instagram.com/p/CPkgc--NkhZ/).

### Download all posts from a user
```bash
python3 . --user yoo__sha
```

It will download all contents from [here](https://instagram.com/yoo__sha).

### Download story from a user
```bash
python3 . --story yoo__sha
```

A chrome tab will be opened. Login with your IG account. (**It doesn't take your credentials**)

### Options

* `--verbose` or `-V` : Print verbose things

## Tested Environments

- MacBook Pro (15-inch, 2018)
  - Python 3.9.4 64-bit
  - macOS Big Sur 11.3.1

- Mac mini (M1, 2020)
  - Python 3.9.4 arm64
  - macOS Big Sur 11.5 beta 2 (20G5033c)