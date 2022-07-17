# bbchallenge API

This code is the backend of [https://bbchallenge.org](https://bbchallenge.org).

## Installing bbchallenge-api

```sh
python3.9 -m venv venv
source venv/bin/activate
```

Two cases:

- production: `pip install -r requirements.txt`
- development: `pip install -r requirements-dev.txt`

You will need an extra package, `dichoseek` which is not currently packaged but available at [https://github.com/tcosmo/dichoseek](https://github.com/tcosmo/dichoseek).

One way to install it is:

```sh
cd ~/Downloads
git clone https://github.com/tcosmo/dichoseek
cd /path/to/bbchallenge-api
ln -s ~/Downloads/dichoseek/dichoseek venv/lib/python3.9/site-packages/dichoseek
```

## Running bbchallenge-api

`bbchallenge-api` relies on several binary files:

- The [seed database](https://bbchallenge.org/method#download) of bbchallenge, path to it is specified in `config.py/DB_PATH`
- The [undecided index file](https://github.com/bbchallenge/bbchallenge-undecided-index) of bbchallenge, path to it is specified in `config.py/DB_PATH_UNDECIDED`
- All the index files of decided machines, currently available at [http://docs.bbchallenge.org/bb5_decided_indexes/](http://docs.bbchallenge.org/bb5_decided_indexes/). Path to their containing folder is specified in `config.py/DB_PATH_DECIDED`

Once you have setup these files, you are good to go with:

- production: `python run_gunicorn.py`
- development: `python run.py`