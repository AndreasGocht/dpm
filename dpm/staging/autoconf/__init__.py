from dpm.downloader import WebResource, File
from dpm.pkg_definition import Aspect, BasePackageRecipe

from dpm.types import Needs

# Usually, the preconfigured tar balls should be used wherever possible
# With HDF5, there is an annoying bug, where
# -lsr-complexity-limit=131072


class PackageRecipe(BasePackageRecipe):
    def __init__(self, store, name):
        super().__init__(store, name)

    def needs(self) -> list[Needs]:
        return [Needs("cc"), Needs("xz"), Needs("git"), Needs("base")]

    def aspects(self) -> list[Aspect]:
        return [Aspect.CONTAINS_BINARIES]

    def sources(self):
        return [
            WebResource(
                self,
                "https://alpha.gnu.org/pub/gnu/autoconf/autoconf-2.72e.tar.xz",
            ),
            File(self, "0001-Port-better-to-NVHPC.patch"),
        ]

    def prepare(self):
        self.tmpdir_execute(
            ["patch", "-p1", "-i", "../0001-Port-better-to-NVHPC.patch"],
            subdir="autoconf-2.72e",
        )

    def create(self):
        self.configure(
            "../autoconf-2.72e/",
            [
                "--enable-static",
                "--disable-shared",
            ],
        )
        self.make()

    def install(self):
        self.make("install")
