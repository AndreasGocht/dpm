class Resource:
    def __init__(self, pkg: "dpm.pkg_definition.BasePackageRecipe"):
        self.pkg: "dpm.pkg.BasePackageRecipe" = pkg

    def download(self) -> None:
        pass
