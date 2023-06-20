import logging
import inspect
import typing
import builtins

logging.root.setLevel(logging.DEBUG)
_logger = logging.getLogger(__name__)


class IoCResolvable(typing.Protocol):
    def resolve(self, **kwargs):
        ...


class IoCDependency:
    def __init__(self, container, key, **kwargs):
        self._container = container
        self._key = key
        self._kwargs = kwargs

    def resolve(self, **kwargs):
        merged_kwargs = self._kwargs.copy()
        merged_kwargs.update(kwargs)
        return self._container.resolve(self._key, **merged_kwargs)


class IoCInstanceEntry:
    def __init__(self, instance):
        self._instance = instance

    def resolve(self, **kwargs):
        if kwargs:
            raise TypeError(f"Cannot pass kwargs to instance {self._instance}")
        return self._instance


class IoCFactoryEntry:
    def __init__(self, factory, **kwargs):
        self._factory = factory
        self._kwargs = kwargs

    def resolve(self, **kwargs):
        merged_kwargs = self._kwargs.copy()
        merged_kwargs.update(kwargs)
        for key, value in merged_kwargs.items():
            if isinstance(value, IoCDependency):
                resolved = value.resolve()
                merged_kwargs[key] = resolved
        return self._factory(**merged_kwargs)


class IoCContainer:
    def __init__(self):
        self._registry: typing.Dict[type, IoCResolvable] = dict()

    def register(self, key: type, item: typing.Any) -> None:
        _logger.debug(f"Registering {item} with key {key}")
        if key in vars(builtins).values():
            raise TypeError(f"Key cannot be a builtin, got {key}")
        if not inspect.isclass(key):
            raise TypeError(f"Key must be a class, got {key}")
        if key in self._registry:
            raise KeyError(f"Key {key} is already registered")

        if inspect.isclass(item):
            self._register_class(key, item)
        elif callable(item):
            self._register_factory(key, item)
        else:
            self._register_instance(key, item)

    def _register_class(self, key: type, item: type) -> None:
        wrapped_args = {}
        spec = inspect.getfullargspec(item.__init__)

        arg_names = spec.args[1:]
        arg_count = len(arg_names)

        cutoff = arg_count - len(spec.defaults) if spec.defaults else arg_count

        for name in arg_names[:cutoff]:
            if name not in spec.annotations:
                raise TypeError(f"Argument {name} of {item} is missing a type hint")
            wrapped_args[name] = IoCDependency(self, spec.annotations[name])

        for n, name in enumerate(arg_names[cutoff:]):
            if name not in spec.annotations:
                raise TypeError(f"Argument {name} of {item} is missing a type hint")
            wrapped_args[name] = spec.defaults[n]

        self._registry[key] = IoCFactoryEntry(item, **wrapped_args)

    def _register_factory(self, key: type, item: typing.Callable) -> None:
        hints = typing.get_type_hints(item)
        if 'return' not in hints:
            raise TypeError(f"Callable {item} must have a return type hint")

        if issubclass(hints['return'], key):
            raise TypeError(f"Callable {item} must return a type that is a subclass of {key}")

        self._registry[key] = IoCFactoryEntry(item)

    def _register_instance(self, key: type, item: typing.Any) -> None:
        if not inspect.isclass(item.__class__):
            raise TypeError(f"Item must be a class or an instance of a class, got {item}")

        self._registry[key] = IoCInstanceEntry(item)

    def resolve(self, key, **kwargs) -> typing.Any:
        if key not in self._registry:
            raise KeyError(f"No item found with key: {key}")
        return self._registry[key].resolve(**kwargs)

    def unregister(self, key: type):
        if key not in self._registry:
            raise KeyError(f"No item found with key: {key}")
        self._registry.pop(key, None)

    def __contains__(self, item: type):
        return item in self._registry

    def clear(self):
        self._registry.clear()

    def __len__(self):
        return len(self._registry)


class IoCInstance(type):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        base = dct.get('__ioc_base__', bases[0] if bases else cls)
        IoCContainer.register(base, cls)