Golden Rules
============


The purpose of DPM is to create straightforward working software
----------------------------------------------------------------

Everything else is secondary to this goal.

If an ugly hack makes it possible to deliver working software in  more cases, use it.

If a recipe works, but might sometimes errornously use system libraries, live with it.


Be minimally opinionated about the operating system
---------------------------------------------------

To create straightforward working software for many users, we can not be opinionated about the operating system.

If the system GCC, that we wrap is a an ancient 8.5.0 on some RHEL clone, live with it.

If there are lib64 vs lib special cases, try to live with with them.

Be minimally opinionated about the software to install
------------------------------------------------------

The same thing applies to the software to be installed too.

If this achieves more straightforward, working, software, live with any choices the program does.

Use static linking everywhere
-----------------------------

Dynamic linking is an invitation for the software to select the wrong shared library at any given opportunity.

At the cost of larger binaries, this creates software that once it is build, uses the correct libraries.

This does not override the previous golden rule.

If a software is unable to create good, working, static libraries.


DPM is only concerned with languages without a package manager
--------------------------------------------------------------

This usually means C, C++, Fortran.

We do not package Rust, Python, etc. just because we can. Those languages
are better suited by their own ``cargo``, ``pip``, etc.

Exceptions are things like the python-implemented Ninja, that are required to build
other software.

We are trying to solve problems where there is no good solution yet.
