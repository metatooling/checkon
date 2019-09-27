import typing as t

import attr
import marshmallow_dataclass
import pyrsistent

from . import schemas


@attr.s(auto_attribs=True)
class VersionInfo:
    major: int
    minor: int
    micro: int
    releaselevel: str
    serial: int

    @classmethod
    def from_tuple(cls, tup):
        return cls(tup)


@attr.s(auto_attribs=True)
class Python:
    is_64: bool
    version_info: t.Tuple[int, int, int, str, int]
    executable: str
    name: str
    sysplatform: str
    version: str


@attr.s(auto_attribs=True)
class Setup:
    retcode: int
    output: str
    command: t.List[str] = attr.ib(converter=pyrsistent.freeze)


@attr.s(auto_attribs=True)
class Test:
    retcode: int
    output: str
    command: t.List[str] = attr.ib(converter=pyrsistent.freeze)


@attr.s(auto_attribs=True)
class InstallPkg:
    sha256: str
    basename: str


@attr.s(auto_attribs=True)
class TestEnv:

    python: Python
    setup: t.List[Setup]
    name: t.Optional[str]
    test: t.Optional[t.List[Test]] = None
    installpkg: t.Optional[InstallPkg] = attr.ib(default=None)
    installed_packages: t.List[str] = attr.ib(converter=pyrsistent.freeze, factory=list)

    @classmethod
    def from_dict(cls, data, name):
        cls(**data, name=name)


@attr.s(auto_attribs=True, frozen=True)
class ToxRun:
    toxversion: str
    commands: t.List[t.Any] = attr.ib(converter=pyrsistent.freeze)
    platform: str
    host: str
    testenvs: t.Dict[str, TestEnv] = attr.ib(
        converter=lambda d: {k: attr.evolve(v, name=k) for k, v in d.items()}
    )
    reportversion: str

    @classmethod
    def from_path(cls, path):
        schema = schemas.class_schema(cls)()
        with open(path) as f:
            return schema.loads(f.read())
