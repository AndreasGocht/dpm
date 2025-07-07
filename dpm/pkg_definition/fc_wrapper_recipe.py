import pathlib

from dpm.types import Provides, Needs

from .wrapper_recipe import WrapperPackageRecipe


class FCWrapperPackageRecipe(WrapperPackageRecipe):
    def __init__(self, store, name: str, toolchain: str, fc):
        super().__init__(store, name, [fc])
        self.toolchain = toolchain
        self.fc = fc

    def fc_compiler_path(self) -> pathlib.Path:
        return self.prefix / "bin" / self.fc

    def needs(self) -> list[Needs]:
        return [Needs(self.toolchain + "_cc")]

    def env_hook(self, env):
        env.env["FC"] = str(self.fc_compiler_path())
        env.env["F77"] = str(self.fc_compiler_path())

    def provides(self) -> list[Provides]:
        return [Provides("fc"), Provides(self.toolchain + "_fc")]
