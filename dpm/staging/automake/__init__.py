from dpm.downloader import WebResource
from dpm.pkg_definition import Aspect, BasePackageRecipe

from dpm.types import Needs


# Usually, the preconfigured tar balls should be used wherever possible
# With HDF5, there is an annoying bug, where
# -lsr-complexity-limit=131072 is interpreted as
class PackageRecipe(BasePackageRecipe):
    def __init__(self, store, name):
        super().__init__(store, name)

    def needs(self) -> list[Needs]:
        return [Needs("cc"), Needs("git"), Needs("base")]

    def aspects(self) -> list[Aspect]:
        return [Aspect.CONTAINS_BINARIES]

    def sources(self):
        return [
            WebResource(
                self, "https://alpha.gnu.org/gnu/automake/automake-1.17.92.tar.gz"
            ),
        ]

    def prepare(self):
        pass

    def create(self):
        self.configure(
            "../automake-1.17.92/",
            [
                "--enable-static",
                "--disable-shared",
            ],
        )
        self.make()

    def install(self):
        self.make("install")
