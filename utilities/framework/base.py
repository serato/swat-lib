# coding: utf-8
"""
Shared base framework classes for web team
Don't forget to document anything you add here ಠ_ಠ
"""

import os
import re

import yaml
import json
import logging


def _findpath(dct, key, path=()):
    """
    Find the first path to a given key in a nested dict
    Maybe update to this if the dict gets too big to recurse:
    http://garethrees.org/2016/09/28/pattern/
    """
    for k, v in dct.items():
        if k == key:
            return True, path + (k,)
        if isinstance(v, dict):
            found, pth = _findpath(v, key, path + (k,))
            if found:
                return True, pth
    return False, None


class obj(object):
    """
    Simple class to turn a nested dict into an object, so you can
    use a.b.c instead of a['b']['c']`
    """
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
               setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
            else:
               setattr(self, a, obj(b) if isinstance(b, dict) else b)


def dict_merge(a, b):
    """
    Merges two dictionaries, combining their keys/values at each level of nesting. If keys are duplicated between
    dictionaries, the values in the latter dictionary (b) will override those in the former (a).

    (This is different from a regular dict.update() in that it is recursive, rather than only looking at the top level.)
    """
    to_update = dict(a)

    for k, v in b.items():
        if isinstance(v, dict):
            to_update[k] = dict_merge(a.get(k, {}), v)
        else:
            to_update[k] = v

    return to_update


def dict_map_leaves(nested_dicts, func_to_call):
    """
    Applies a given callable to the leaves of a given tree / set of nested dictionaries, returning the result (without
    modifying the original dictionary)

    :param nested_dicts: Nested dictionaries to traverse
    :param func_to_call: Function to call on the 'leaves' of those nested dictionaries
    :return: Result of the transformation (dict)

    Note that this and all the functions above use the exact same algorithm/pattern for tree traversal. We could reduce
    duplication by refactoring it into a function, but that might make the code less readable.
    """
    to_update = dict(nested_dicts)

    for k, v in nested_dicts.items():
        if isinstance(v, dict):
            to_update[k] = dict_map_leaves(v, func_to_call)
        else:
            to_update[k] = func_to_call(v)

    return to_update


class Configuration(object):
    """
    Base configuration object for storing grouped configuration sets
    e.g. different values for environment names, etc.
    """
    def __init__(self, rootkey=None):
        self.data = {}
        self.scoped = None
        self.rootkey = rootkey
    
    def load(self, filename):
        with open(filename, 'r') as f:
            self.data = dict_merge(self.data, yaml.load(f, Loader=yaml.SafeLoader))
        self.scope(self.rootkey)

    def load_env_vars(self, filename):
        """
        Load environment variable names from a YAML file (see env_config_map.yaml)
        """
        with open(filename, 'r') as f:
            env_var_data = yaml.load(f, Loader=yaml.SafeLoader)
        self.load_env_vars_dict(env_var_data)

    def load_env_vars_dict(self, vars_map):
        """
        Load environment variables from a dictionary of configuration values / variable names, where the 'leaves' of the
        nested dictionary tree are names of environment variables to load.

        For example:

        vars_map = {
            'client_apps': {
                'test_automation': {
                    'id': 'TEST_AUTOMATION_APP_ID',
                    'password': 'TEST_AUTOMATION_APP_PASSWORD'
                }
            }
        }
        """
        client_app_data = dict_map_leaves(vars_map, lambda v: os.environ[v])
        self.data = dict_merge(self.data, client_app_data)

    def dump(self):
        print(json.dumps(self.scoped, sort_keys=True, indent=4, separators=(',', ': ')))
    
    def scope(self, key):
        scoped = self.data.copy()
        found, path = _findpath(scoped, key)
        if found:
            for key in path:
                if scoped[key] is not None:
                    scoped.update(scoped[key])
        self.scoped = scoped

    def __getattr__(self, name):
        if name in self.scoped:
            result = self.scoped[name]
            if isinstance(result, dict):
                return obj(result)
            else:
                return result
        else:
            raise AttributeError('No such attribute: {}'.format(name))
    
    def __iter__(self):
        for key in self.scoped:
            yield (key, self.scoped[key])

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass


class Browser():
    def __init__(self, driver):
        self.driver = driver
    
    def get(self, url):
        logging.getLogger().info('GET {}'.format(url))
        return self.driver.get(url)


def set_environment_from_file(env_file_path):
    """
    Sets environment variables from keys/values in a (generally .env) file.
    :param env_file_path: Path of the .env file
    """
    # Captures the variable name and value (ignoring quotes around the value, and spaces around the equals sign)
    env_pattern = re.compile(r'^([^\s=]+)=(?:[\s"\']*)(.+?)(?:[\s"\']*)$')

    # Dictionary of environmental variables
    env_vars = {}

    # Extract the variables from the file, if there are any present
    with open(env_file_path, 'r') as f:
        for line in f:
            match = env_pattern.match(line)
            if match is not None:
                env_vars[match.group(1)] = match.group(2)

    # Add these variables to the environment
    os.environ.update(env_vars)


# TODO: manage lifecycle of licences etc, clean up data from db if necessary
