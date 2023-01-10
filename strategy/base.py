from _utils.validate import val_instance
from strategy.protocol import StrategyResponse

# todo: rewrite docs


class RequiredOverwrite(Exception):
    """ Base class for classes that require an overwrite. """
    pass


class Strategy:
    # @property `config` 'Config'
    # Used to define the `config` class variable which is meant to be a 'Config' type
    # object which contais all required strategy parameters and are to be accesible by the
    # strategy.
    # `config` compatibility is determined by "Strategy.compatibility" and "Config.version"
    # where compatibility is "True" if "Config.version is None" or if "Strategy.compatibility is None"
    # ("Strategy.compatibility is [None]" due to required Iterable of compatibility since compatibility
    # is always checked with "in").
    # `config` is required and can obly be overwritten, trying to delete it will raise an error.
    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, _config: object):
        val_instance(_config, object)

        self._config = _config

    def set_config(self, _config: object) -> None:
        self.config = _config

    @config.deleter
    def config(self):
        raise ValueError(f"`config` can't be deleted, only overwritten.")

    def __init__(self) -> None:

        self.__initvars__()

    def __feed__(self, *args) -> bool:
        return True

    def next(self, *args) -> StrategyResponse:
        raise RequiredOverwrite(f"`next()` requires overwrite.")
