import re

import yaml
import os
from copy import deepcopy


class YConfig:
    """
        Reads configuration for environment descriptor yaml files with given precedence order
        env-defaulst.yml < env-envs1.yml < env-envs2.yml ... etc.
        All yaml descriptor file should follow the pattern 'env-*.yml' and should be stored in same config folder
        (i.e. yamls) and path of this config folder should be passed as base_path
    """
    def __init__(self, base_path=None, envs=None):
        self.parsed_yaml = None
        self.config = None
        self.prefix = 'env-'
        self.suffix = '.yml'
        self.defaults = 'defaults'
        # based on https://stackoverflow.com/a/52428766
        if not [x for x in (base_path, envs) if x is None]:
            self.set_config(base_path, envs)

    def set_config(self, base_path, envs):
        self.config = self.read_configuration(base_path, envs)

    def read(self, base_path, file_name):
        path_join = os.path.join(base_path, file_name)
        with open(path_join, 'r') as stream:
            try:
                self.parsed_yaml = yaml.safe_load(stream)
                return self.parsed_yaml
            except yaml.YAMLError as exc:
                print(exc)

    def read_env_dict(self, base_path, env):
        file_name = self.prefix + env + self.suffix
        return self.read(base_path, file_name)

    def read_configuration(self, base_path, envlist):
        result = self.read(base_path, self.prefix + self.defaults + self.suffix)
        for env in envlist:
            file_name = self.prefix + env + self.suffix
            env_conf = self.read(base_path, file_name)
            result = self.dict_of_dicts_merge(result, env_conf)
        return result

    # This function is based on a similar one in https://stackoverflow.com/a/26853961
    def dict_of_dicts_merge(self, x, y):
        r = {}
        if type(x) == dict and type(y) == dict:
            overlapping_keys = x.keys() & y.keys()
            for key in overlapping_keys:
                r[key] = self.dict_of_dicts_merge(x[key], y[key])
            for key in x.keys() - overlapping_keys:
                r[key] = deepcopy(x[key])
            for key in y.keys() - overlapping_keys:
                r[key] = deepcopy(y[key])
        elif type(x) == dict:
            for key in x.keys():
                r[key] = deepcopy(x[key])
        elif type(y) == dict:
            for key in y.keys():
                r[key] = deepcopy(y[key])
        else:
            r = y
        return r

    def get(self, key):
        if self.config is None:
            raise RuntimeError('Configuration should be initialized')
        return aget(self.config, tokenize(key))


# The following code was obtained from shyaml -- https://github.com/0k/shyaml

class NonDictLikeTypeError(TypeError):
    """Raised when attempting to traverse non-dict like structure"""


class IndexNotIntegerError(ValueError):
    """Raised when attempting to traverse sequence without using an integer"""


class IndexOutOfRange(IndexError):
    """Raised when attempting to traverse sequence without using an integer"""


class MissingKeyError(KeyError):
    """Raised when querying a dict-like structure on non-existing keys"""

    def __str__(self):
        return self.args[0]


def tokenize(s):
    r"""Returns an iterable through all subparts of string splitted by '.'

    So:

        >>> list(tokenize('foo.bar.wiz'))
        ['foo', 'bar', 'wiz']

    Contrary to traditional ``.split()`` method, this function has to
    deal with any type of data in the string. So it actually
    interprets the string. Characters with meaning are '.' and '\'.
    Both of these can be included in a token by quoting them with '\'.

    So dot of slashes can be contained in token:

        >>> print('\n'.join(tokenize(r'foo.dot<\.>.slash<\\>')))
        foo
        dot<.>
        slash<\>

    Notice that empty keys are also supported:

        >>> list(tokenize(r'foo..bar'))
        ['foo', '', 'bar']

    Given an empty string:

        >>> list(tokenize(r''))
        ['']

    And a None value:

        >>> list(tokenize(None))
        []

    """
    if s is None:
        return
    tokens = (re.sub(r'\\(\\|\.)', r'\1', m.group(0))
              for m in re.finditer(r'((\\.|[^.\\])*)', s))
    # an empty string superfluous token is added after all non-empty token
    for token in tokens:
        if len(token) != 0:
            next(tokens)
        yield token


def aget(dct, key):
    r"""Allow to get values deep in a dict with iterable keys

    Accessing leaf values is quite straightforward:

        >>> dct = {'a': {'x': 1, 'b': {'c': 2}}}
        >>> self.aget(dct, ('a', 'x'))
        1
        >>> self.aget(dct, ('a', 'b', 'c'))
        2

    If key is empty, it returns unchanged the ``dct`` value.

        >>> self.aget({'x': 1}, ())
        {'x': 1}

    """
    key = iter(key)
    try:
        head = next(key)
    except StopIteration:
        return dct

    if isinstance(dct, list):
        try:
            idx = int(head)
        except ValueError:
            raise IndexNotIntegerError(
                "non-integer index %r provided on a list."
                % head)
        try:
            value = dct[idx]
        except IndexError:
            raise IndexOutOfRange(
                "index %d is out of range (%d elements in list)."
                % (idx, len(dct)))
    else:
        try:
            value = dct[head]
        except KeyError:
            # Replace with a more informative KeyError
            raise MissingKeyError(
                "missing key %r in dict."
                % (head,))
        except Exception:
            raise NonDictLikeTypeError(
                "can't query subvalue %r of a leaf%s."
                % (head,
                   (" (leaf value is %r)" % dct)
                   if len(repr(dct)) < 15 else ""))
    return aget(value, key)
