import pathlib
import urllib.parse
import urllib.request

from .resource import Resource
from dpm.helpers import UrlretrieveProgressHelper


class WebResource(Resource):
    def __init__(self, pkg: "dpm.pkg_definition.BasePackageRecipe", url):
        super().__init__(pkg)
        self.url = url

    def download(self):
        filename = pathlib.Path(urllib.parse.urlparse(self.url).path).name
        print(f"Downloading {self.url}")
        urllib.request.urlretrieve(
            self.url,
            filename=self.pkg.tmpdir / filename,
            reporthook=UrlretrieveProgressHelper(),
        )

        filename = pathlib.Path(urllib.parse.urlparse(self.url).path).name
        if ".tar" in filename:
            self.pkg.tmpdir_execute(["tar", "xf", filename])
