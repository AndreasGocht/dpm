Command Line Interface
==========================

Synopsis
--------

**dpm**

DPM is controlled through the **dpm.py** Python script in the root of the repository.
DPM is invoked as:

``$./dpm.py <arguments_to_dpm> <subcommand> <arguments_to subcommand>``.

Global Options
--------------

.. program:: dpm

.. _make_node:

.. option:: -v, --verbose 

   Enable more debug output

Subcommand ``install``
----------------------

**dpm install <store> <package>**

Install the package *<package>* to the store *<store>*, recursively installing all further dependencies.
If *<package>* is already installed, this command does nothing.
The install command currently might require interactive attention, and as such can not be embedded in scripts.
A user is asked, for example, which C/C++ compiler suite to use.

Stops and prints an error if it is not possible to install *<package>* to *<store>*.
Reasons are:

1. *<package>* or a dependency of *<package>* conflict with an already installed package.
2. Installing *<package>* requires a package in a variant that it is not installed as, or which is actively forbidden by another package. 

Options
~~~~~~~

.. option:: -r, --required <variant>

   Requires *<package>* to be installed with *<variant>* as a required variant.
   ``install`` fails if this required *<variant>* is forbidden by another package to install or in the store.


.. option:: -f, --forbidden <variant>

   Forbids *<package>* to be installed with *<variant>* enabled.
   If the forbidden *<variant>*

       1. is required for *<package>* by a package already installed in the store
       2. is required for *<package>* by a dependency of *<package>*
       3. conflicts with another forbidden or required variant of *<package*>
   
   installation fails.

Subcommand ``stored``
---------------------

**dpm stored <store>**

Lists all packages stored in *<store>* and their required/forbidden variants.

Subcommand ``uninstall``
------------------------

**dpm uninstall <store> <package>**

Uninstalls *<package>* from *<store>*.

Currently fails if any other package installed in *<store>* depends on *<package>*

Subcommand ``shell``
--------------------

**dpm shell <store> <package1>, <package2>, ..., <packagen>**

Starts a ``bash`` shell with all environment variables (``$PATH``, ``$PKG_CONFIG_LIBDIR``,...) set to the paths of the packages
*<package1>*, *<package2>*, ..., *<packagen>*.
