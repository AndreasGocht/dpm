Basics
======

DPM is responsible for installing software from a repository into a store, which is a path managed by DPM.
While it offers many choices for a package class, e.g. such as GCC, Clang, etc. for the *<package class>* *<pkg_class<cc>*, aswell as
different variants of packages, only one package of any package class, or on combination of variants might be installed in a store.

If you need both GCC and Intel Compiler versions of some package, the solution is installing them into separate stores.

The list below offers definitions for common terms in DPM.


**<store>**
   A *<store>* is a location for DPM to install packages to.

   For every package installed in DPM, a folder ``<store>/<pkgname>/`` and a file ``<store>/<pkgname>.spec`` is created.
   ``<store>/<pkgname>/`` is the prefix of the package *pkg<pkgname>* in the store *<store>*.
   This will, depending on the package, contain subfolders such as ``bin/``, ``lib/``, as usually installed into `/usr` in a system-wide install.
   ``<store>/<pkgname>.spec`` is a JSON file recording metadata for the installed packages.
   It records, for example, the enabled and disabled variants.

   For every *<package class>* only one concrete package can be installed in any store.
   The same store can not contain multiple C compilers, for example.
   This should make it easier to not get confused (and likely broken) builds that choose incompatible versions of the same library, at the expense of duplicating some dependencies.
   Management of the *<store>* should be left to DPM, modifying anything in that 
   The simplest way to deal with a broken store is to delete it and reinstall.

**<package class>**
   A *<package class>* is a class of concrete *<packages>* that provide the same functionality.
   *pkg_class<cc>* is the class of all C compilers available in DPM.
   
   Every package is always implicitely its own package class.
   The *pkg<foobar>* always implies *pkg_class<foobar>*.

**<package>**
   A concrete, installable package.
   Every *<package>* in DPM comes with a package recipe, located in ``dpm/repo/<pkgname>/`` which gives is needs
   as well as the instructions for building it.

**<provides>**
   The concept, aswell as the dpm Python class ``dpm.Provides`` that denotes that a package provides some *<pkg_class>* other than itself.
   With *provides<cc>* a recipe shows, that the current package provides the functionality of a C compiler.

   If a package that *provides<foobar>* is installed, no other package that *provides<foobar>* can be installed into that *<store>*.
   Similiarly installing a package that *provides<foobar>* into a *<store>* that already has a package that *provides<foobar>* will fail.

**<needs>**
   The concept, aswell as the dpm Python class ``dpm.Needs`` that denotes that this package *<needs>* at build-time or run-time
   another package.
   When installing a package the DPM solver will check if any package of the *<needed>* package class can be installed, prompting
   the user to select one if there are multiple options and then installing them before *<package>*.

**<forbids>**
   The inverse of **<needs>**, the concept aswell as the Python class ``dpm.Forbids`` denoting that the given *<package>* and the forbidden
   one can not co-exist.

   An example of this is *pkg<elfutils>*, which can not be compiled with *pkg<intel_cc>* due to the use of features not supported by the classic Intel Compiler.
   Any attempt to install a package forbidding *pkg_class<foobar>* into a *<store>* where *pkg_class<foobar>* is already installed, will fail.
   Similiarly the solver will deselect any *<package>* that depends on (or is of) that forbidden package class.

**<variant>**
   Depending on the features enabled, the same *<package>* can come in multiple, possibly incompatible *<variants>*.
   A single (installed) package can have multiple compatible *<variants>* at the same time.

   Other packages, aswell as the user can request ("require") certain package variant, aswell as ("forbid") others.

   *<variants>* come in four classes:

   *required* (for installed packages, also called *enabled*)
      This variant of the package is *required*, either because the package is already installed or because
      some package in the dependency chain of the package-to-be-installed requires it.
      Trying to install a package that *forbids* this variant of a package into a store where this package with this variant enabled 
      is already installed, is not possible.
   
   *default*
      This variant of the package will be installed by default, but can actively be forbidden by the user or another package.
      If it is forbidden, the variant moves to the forbidden variant class during install.
      If it is not forbidden, the variant moves to a required variant.

      This class of variants contain features useful to many users, but which might lead to problems with some packages.

   *optional*
      This variant is only enabled if it is explicitly required by the user or another package.
      If it is explicitly required, it is promoted to a required variant on install.
      It if is not, it is demoted to a forbidden variant.

      Optional variants are useful for features that might create issues with the majority of packages or for features
      which put undue burden on the user.
      A common example is any kind of NVidia CUDA support, as this requires the user to install a multi-GiB CUDA compiler
      toolkit and have NVidia hardware which can actually make use of the feature.

   *forbidden* (for installed packages, also called *disabled*)
      This variant is forbidden, either because a package is already installed with the given variant disabled or because
      the user or another package forbids it use.
      Installing a package that requires this variant of a package into a store where this package with this variant disabled
      is already installed, is not possible.
