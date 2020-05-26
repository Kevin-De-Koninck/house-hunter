import sys
from logzero import logger


class Anon_kwargs:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Anon_dict:
    def __init__(self, dictionary):
        for k, v in dictionary.items():
            if isinstance(v, dict):
                setattr(self, k, Anon_dict(v))
            else:
                setattr(self, k, v)


class Helpers:
    # Much faster (but simpler) deepcopy implementation that is sufficient for the needs of this script
    @staticmethod
    def deepcopy(original):
        new = dict().fromkeys(original)
        for k, v in original.items():
            try:
                new[k] = v.copy()  # dicts, sets
            except AttributeError:
                try:
                    new[k] = v[:]  # lists, tuples, strings, unicode
                except TypeError:
                    new[k] = v  # int
        return new

    @staticmethod
    def convert_to_value(yaml_expression, dictionary):
        value = Helpers.deepcopy(dictionary)
        try:
            for key in yaml_expression.split('.'):
                value = value[key]
                if value is None:
                    break
        except (AttributeError, KeyError):
            logger.error("Key '%s' does not exist in the following dictionary:\n%s'",
                         yaml_expression, repr(dictionary))
            sys.exit(1)
        return value

