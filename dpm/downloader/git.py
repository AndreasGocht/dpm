import pathlib
import urllib.parse

from .resource import Resource

from dpm.types import Needs


class Git(Resource):
    def __init__(self, pkg: "dpm.pkg_definition.BasePackageRecipe", url: str, checkout):
        super().__init__(pkg)
        self.url = url
        self.checkout = checkout

        if Needs("git") not in self.pkg.needs():
            raise RuntimeError(
                "Packages that download things from git should depend on git !"
            )

    def download(self):
        self.pkg.tmpdir_execute(["git", "clone", self.url])

        dirname = pathlib.Path(urllib.parse.urlparse(self.url).path).stem
        self.pkg.tmpdir_execute(["git", "checkout", self.checkout], subdir=dirname)
        self.pkg.tmpdir_execute(
            ["git", "submodule", "update", "--init", "--recursive"],
            subdir=dirname,
        )
