# InstagramDL

> Download Instagram posts and stories simply

## Disclaimer

We do not have responsibiliy for you to download explict, harmful things.

**Use at your own risk!**

## Usage

InstagramDL requires your instagram account to authenticate with Instagram server.

It will be used only in grabbing cookies, which is used in querying Instagram GraphQL API.

**We do not take your credentials, and honestly we do not want to know.**

### Download only a post
```bash
python3 . --post CPkgc--NkhZ --login <YOUR_ID> --pw <YOUR_PW>
```

It will download contents from [here](https://www.instagram.com/p/CPkgc--NkhZ/).

### Download all posts from a user
```bash
python3 . --user yoo__sha --login <YOUR_ID> --pw <YOUR_PW>
```

It will download all contents from [here](https://instagram.com/yoo__sha).

### Download story from a user
```bash
python3 . --user yoo__sha --stories --login <YOUR_ID> --pw <YOUR_PW>
```

It will download stories from [here](https://instagram.com/yoo__sha).

### Options

* `--verbose` or `-V` : Print verbose things

## Tested Environments

- MacBook Pro (15-inch, 2018)
  - Python 3.9.4 64-bit
  - macOS Big Sur 11.3.1

- Mac mini (M1, 2020)
  - Python 3.9.4 arm64
  - macOS Big Sur 11.5 beta 2 (20G5033c)


## Contributing

PR or make a issue

### Code style

* black + isort
* Class names as `Pascal`
* Variable and function names as `snake`
