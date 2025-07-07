Introduction
============

Installing software is easy until it's not.

If you are working in High-Performance-Computing, you have probably encountered situations where some software is not available, either as a system package or as a module.
Containerization in HPC, if it is available is often its own can of worms.
And hassling your HPC administrators is then often not worth your or theirs time for the one-off experiments you are performing.

It has atleast occured to me pretty often and then I have dreamed of the fastest way to go from A to working software. The Dresden Package Manager (DPM) is such a software.

Only requiring a quite ancient Python 3 version, DPMs only job is to install packages from its repository to a user-specified directory.

It tries to, atleast for me, do this job simpler and more straightforward than more fully-features packaging options, such as Spack, NixOS and Homebrew, at the expense of any correctness guarantees other than creating *working* software.

May this software be useful to others, too.
