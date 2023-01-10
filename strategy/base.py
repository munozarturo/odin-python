from types import UnionType
from typing import Type

from _utils.keyword import iskeyword as _iskeyword
from _utils.typing import Version, NoneType, Iterable
from _utils.validate import val_instance, LogWarning
from strategy.protocol import StrategyResponse, Trade

# todo: rewrite docs


class RequiredOverwrite(Exception):
    """ Base class for classes that require an overwrite. """
    pass


class Config:
    def __init__(self, version: Version | None = None):
        self._version: Version = None
        self.version: Version = version

    def __hash__(self) -> int:
        return hash(tuple(self.as_list()))

    def __eq__(self, __o: object) -> bool:
        return hash(__o) == hash(self)

    def as_dict(self):
        pass

    def as_list(self):
        pass

    def as_tuple(self):
        pass

    def to_json(self):
        pass

    def to_csv(self):
        pass


def from_dict():
    pass


def from_list():
    pass


def from_tuple():
    pass


def from_json():
    pass


def from_csv():
    pass


def config(version: Version, parameters: list | tuple[list | tuple]) -> Config:
    # `function needs to generate a config object that
    # houses all parameters for an algorithm and these
    # objects can be imported from aliased versions
    # that can be generated with this function.`

    # `it's all about finding out how to use the @property
    # decorator dynamically.`

    val_instance(version, str)
    val_instance(parameters, (list, tuple))

    if version.isidentifier():
        raise ValueError(f"Version must be valid identifiers: {version!r}")
    if _iskeyword(version):
        raise ValueError(f"Version cannot be a keyword: {version!r}")

    seen = set()
    for param_index, parameter in enumerate(parameters):
        if not isinstance(parameter, (list, tuple)):
            raise TypeError(
                f"Expected `Iterable` for every element in `parameters`.")

        if len(parameter) != 4:
            raise ValueError(
                f"expected [name, type, validation function, default value], got {parameters[param_index]!r}")

        name, _type, val_func, def_val = parameter

        if _iskeyword(name):
            raise ValueError(
                f"Type names and field names cannot be a keyword: {version!r}")

        if not _type is None:
            if not isinstance(_type, (type, Type, UnionType)):
                raise TypeError(
                    f"in `parameters`, in {parameters[param_index]!r} expecting: [name, type, validation function, default value], `type` must be a of type 'type', 'UnionType', or 'NoneType'.")

        if not val_func is None:
            if not callable(val_func):
                raise TypeError(
                    f"in `parameters`, in {parameters[param_index]!r} expecting: [name, type, validation function, default value], `valiation function` must be callable.")

        if not def_val is None:
            if not _type is None:
                if not isinstance(def_val, _type):
                    raise TypeError(
                        f"in `parameters`, in {parameters[param_index]!r} expecting: [name, type, validation function, default value], `default value` must be of type `type` ({_type!r}).")

        if name.startswith('_'):
            raise ValueError(f"Field names cannot start with an underscore: {name!r}")
        if name in seen:
            raise ValueError(f"Encountered duplicate field name: {name!r}")
        seen.add(name)

        # got up to field defaults


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

    def __init__(self, config: object, version: Version | None = None,
                 compatibility: Version | Iterable[Version] | None = None) -> None:
        """
        Stategy base class.

        When creating a strategy class inherit from the Strategy base class.

        Recommended usage:

        ```
        from strategy import config, Strategy

        # todo add config definition

        class MyStrategy(Strategy):
            def __init__(self, config: object, version: Version | None = None, compatibility: Version | Iterable[Version] | None = None) -> None:
                super().__init__(config, version, compatibility) # super initialization

            # `recommended method for variable initialization
            # note there is no requirement to create this method
            # the only two methods that require and override are the
            # next() method because they are called by
            # other Odin components.`
            def __initvars__(self):
                ...

            # todo: add on_data definition
            def on_data(self, *args):
                ...

            # `the __feed__() method gets called before every next() method call
            # to check whether to call the next() method. this is meant to quicken
            # the run time. eg. if a strategy only trades between 9:30 and 12:00
            # the condition can be written in this function. assuming that 
            # args=(time, price), we can add a condition like the one commented below.
            # if not defined, this function will always default to True.
            #  
            # usage in feeder:
            #   if Strategy.__feed__(args):
            #       Strategy.next(args)
            # `
            def __feed__(self, *args):
                # import datetime as dt
                # return time > dt.time(9, 30) and time < dt.time(12):

                return True

            # `the next() method mimics how a live trading algorithm would work.
            # there are periodic data updates which will change how the strategy
            # behaves. for example, if the data consists of second by second data
            # then the next() method will be called with the data given to the feed.`
            def next(self, *args) -> None | StrategyResponse:
                ...

        ```

        Args:
            config (object): Strategy configuration object.
            version (Version | None, optional): Strategy version. Defaults to None. If version is None then there is implied compatibility with all strategy versions.
            compatibility (Version | Iterable[Version] | None, optional): single compatible config Version or iterable of compatible config Versions. Defaults to None. If compatibility is None then there is implied compatibility with all config versions.
        """

        self._version: Version | NoneType = None
        self._compatible: Version | Iterable[Version] | NoneType = [None]
        self._config: Config = None

        self.version: Version = version
        self.compatibility: Version | Iterable[Version] = compatibility
        self.config = config

        self.__initvars__()

    def __feed__(self, *args) -> bool:
        return True

    def next(self, *args) -> StrategyResponse:
        raise RequiredOverwrite(f"`next()` requires overwrite.")
