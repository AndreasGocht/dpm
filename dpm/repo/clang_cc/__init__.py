import pathlib

from dpm.pkg_definition import WrapperPackageRecipe, Environment
from dpm.store import Store


class PackageRecipe(WrapperPackageRecipe):
    def __init__(self, store: Store, name):
        super().__init__(store, name, ["clang", "clang++"])
        self.cc = "clang"
        self.cxx = "clang++"

    def c_compiler_path(self) -> pathlib.Path:
        return self.prefix / "bin" / "clang"

    def cxx_compiler_path(self) -> pathlib.Path:
        return self.prefix / "bin" / "clang++"

    def toolchain(self) -> str:
        return "clang"

    def env_hook(self, env: Environment):
        env.env["CC"] = str(self.c_compiler_path())
        env.env["CXX"] = str(self.cxx_compiler_path())
