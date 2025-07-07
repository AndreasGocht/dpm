import pathlib

from .aspect import Aspect
from .recipe import BasePackageRecipe


class WrapperPackageRecipe(BasePackageRecipe):
    def __init__(self, store, name, binaries):
        BasePackageRecipe.__init__(self, store, name)
        self.binaries = binaries

    def sources(self):
        return []

    def aspects(self) -> list[Aspect]:
        return [Aspect.CONTAINS_BINARIES, Aspect.VIRTUAL]

    def prepare(self):
        pass

    def create(self):
        pass

    def install(self):
        wrapper_dict = {}
        for binary in self.binaries:
            wrapper_dict[binary] = self.which(binary)

        print(f"Mappings for package {self.name}:")
        for key, value in wrapper_dict.items():
            print(f"\t{key} => {value}")
        answer = ""
        while answer == "":
            answer = input("Is this okay? (y/N): ")
            if answer in {"y", "n"}:
                break
            print(f"Unknown: {answer}. please select y or n")
            answer = ""

        if answer != "y":
            raise RuntimeError("Wrapper resolution wrong!")

        base_bindir = pathlib.Path(self.prefix) / "bin"
        base_bindir.mkdir()
        for key, value in wrapper_dict.items():
            (base_bindir / key).symlink_to(value)
