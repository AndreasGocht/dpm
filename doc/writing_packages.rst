Writing Packages
================

Packages in DPM are described in a self-contained python classes, deriving from ``BasePackageRecipe`` or any of its specializations.

Every package is located in a file ``dpm/<pkgname>/__init__.py``.

Install Process
-------------

1. Execute the DPM solver to see if the package is installable.
2. If the package does not have ``Aspect::VIRTUAL``, create a temporary directory (``Recipe.tmpdir``) for building
3. Create a logfile (``tmpdir/build.log``) the stdout and stderr of all commands of the build process are written into this logfile.
4. Download the sources listed in ``Recipe::sources()`` to ``tmpdir``
5. Call ``Recipe::prepare()`` (Patching files, etc.)
6. Call ``Recipe::create()`` (``./configure``, ``make``, etc.)
7. Create the package prefix in the store, ``<store>/pkgname``
8. Call ``Recipe::install()`` (``make install``, etc.)
9. On success, delete ``tmpdir``

If any of the steps fails (Any of the commands in ``Recipe`` return non-zero). The build immediately fails and ``tmpdir`` is preserved, so that the user can inspect the build failure.

Overridable methods of BasePackageRecipe
----------------------------------------

.. py:module:: dpm 

.. py:class:: BasePackageRecipe
A gifted person ought to learn English (barring spelling and pronouncing) in thirty hours, French in thirty days, and German in thirty years.
   .. py:method:: provides() -> list[Provides]

      Provides the list of <pkgname>s this package provides. For the ``pkg<gcc_wrapper>``, this is ``provides<cc>`` ``provides<gcc>``
      Note that a package always provides itself automatically, e.g. ``pkg<foobar>`` -> ``provides<foobar>`` without explicitly listing it.
   
   .. py:method:: forbids() -> list[Forbids]
      
      Lists the packages that are forbidden to be installed if this package is installed to the ``<store>``. For example ``pkg<elfutils>`` ``forbids<icc>``, because the clasic Intel compiler is unable to build that package.
      A package that ``provides<foobar>`` automatically forbids all packages from being installed in the same ``<store>`` that also ``provides<foobar>``.
      It is not needed to list all the other compilers as "forbids" in a compiler package.

   .. py:method:: needs() -> list[Needs]

      Lists the dependencies of the pkg. For example, ``pkg<elfutils>`` declares, among other things ``needs<cc>``, ``needs<zlib>``.

   .. py:method:: aspects() -> list[Aspects]

      Lists the Aspects of the given package. A definitive description of Aspects is given below. Aspects encode information, such as, "This package contains binaries", which means that ``<store>/<pkgname>/bin`` is added to ``$PATH`` whenever it is required.

   .. py:method:: sources() -> list[Resource]
      
      Gives a list of the sources of the package. A list of all types of Resources is given below.
   .. py:method:: prepare()
      
      Prepares the downloaded files of the packages for further processing. This step is used for applying patches, for example.
   
   .. py:method:: create()
      
      Create the software from the given sources. This includes both the configure/cmake step and the make step in C/C++ applications, for example.

   .. py:method:: install()

      Installs the software into the ``<store>`` corresponds to the ``make install`` step.
       
   .. py:method:: env_hook()

      
Wrapper packages
----------------

A wrapper package is a package that wraps pre-installed software of the underlying system.
The wrapping is done by soft-linking the relevant files from the underlying system to the ``<store>``.

Wrappers are most useful if:

1. The software that it wraps is distributed in sane versions practically universally. (e.g. the ``cat`` wrapper in ``pkg<base>``)
2. The software is difficult to build and the versions found in the wild are mostly sane (e.g. the GCC)
3. The software as deployed contains adaptions to the environment that DPM can not reproduce (e.g. MPIs adapted to the underlying HPC system)

Wrapper package should be named ``pkgname_wrapper``, e.g. ``pkg<cmake_wrapper>``. If an installed version exists, it should be called ``pkgname_inst``, e.g. ``pkg<cmake_inst>``.
Wrapper packages should always ``provide<pkgname>``, e.g. ``provide<cmake>``. Even if currently only the wrapped package exists.

For packages that wrap binaries the convenience class ``WrapperPackageRecipe`` exists.

This takes a list of all the binaries that should be wrapped. They are looked-up at install-time with ``which``, and the user is asked if the found full-paths are correct for the binaries.

For an example of a ``WrapperPackageRecipe`` usage, see ``pkg<base>``.

For an example of a wrapper package that does not use ``WrapperPackageRecipe``, see ``pkg<cuda_wrapper>``.

Aspects
-------

Aspects are used to describe common aspects of packages, such as whether they contain binaries. This currently has three values

``Aspect::CONTAINS_BINARIES``

    The given package contains binaries in the ``<store>/<packge_name>/bin`` directory.
    If `<package>` is a dependency of `<package2>`, then the above path is put into ``$PATH`` when building `<package2>`
    It is also put into the shells' ``$PATH`` when ``dpm shell <package`` is called.

``Aspect::VIRTUAL``

    The package does not build anything. Most common for wrapper packages.

``Aspect::CONTAINS_PKG_CONFIG``
    
    The package contains pkg-config definition files that can be used to find it.
    A package that sets ``Aspect::CONTAINS_PKG_CONFIG`` is added to  ``$PKG_CONFIG_LIBDIR`` in the build of ``<package2>`` if it is a dependency of ``<package2>``

Downloaders
-----------

_TODO_
