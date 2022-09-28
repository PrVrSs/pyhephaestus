import sys
import marshal
from importlib.abc import MetaPathFinder
from importlib.machinery import PathFinder, ModuleSpec, SourcelessFileLoader, SourceFileLoader
from types import CodeType, ModuleType
from typing import Sequence

from more_itertools import first_true

from .constants import PYC_HEADER


class HephaestusLoader:
    loaders: list['HephaestusLoader'] = []

    def __init_subclass__(cls, **kwargs) -> None:
        cls.loaders.append(cls)

    @classmethod
    def get_loader(cls):
        return cls.__mro__[2]


class HephaestusSourceFileLoader(HephaestusLoader, SourcelessFileLoader):
    ...


class HephaestusSourcelessFileLoader(HephaestusLoader, SourceFileLoader):
    ...


def is_loader(loader, loader_b: HephaestusLoader) -> bool:
    return isinstance(loader, loader_b.get_loader())


def hephaestus_loader(loader):
    return first_true(HephaestusLoader.loaders, pred=lambda loader_: is_loader(loader, loader_))


class ImportHook:
    def __enter__(self) -> 'ImportHook':
        if first_true(sys.meta_path, pred=lambda _: isinstance(_, HephaestusMetaPathFinder)) is None:
            sys.meta_path.insert(0, HephaestusMetaPathFinder())

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.meta_path = [
            meta_path_object
            for meta_path_object in sys.meta_path
            if not isinstance(meta_path_object, HephaestusMetaPathFinder)
        ]


def instrument_imports() -> ImportHook:
    return ImportHook()


class HephaestusMetaPathFinder(MetaPathFinder):
    def find_spec(
            self,
            fullname: str, path: Sequence[str] | None,
            target: ModuleType | None = ...
    ) -> ModuleSpec | None:
        spec = PathFinder.find_spec(fullname, path, target)
        if spec is None:
            return

        spec.loader = hephaestus_loader(loader=spec.loader)(spec.loader.name, spec.loader.path)

        return spec


def pyc_loader(file: str) -> CodeType:
    with open(str(file), 'rb') as fd:
        _ = fd.read(PYC_HEADER)
        return marshal.load(fd)
