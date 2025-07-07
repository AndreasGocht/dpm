#!/usr/bin/env python

# Usage: linkcheck.py $STORE
#
# scans the files marked exec in [STORE] for any linked shared libraries that
# are not well known gcc/libc/system/ld-linux libraries that just happen to be
# linked sometimes because GCC refuses to do proper static builds
#

import subprocess

import sys
import pathlib
import stat


def check_libs(pkg, libs):
    for lib in libs:
        # Don't bother with those obvious system/linker/gcc/libc libraries
        if "linux-vdso" in lib:
            continue
        if "libc" in lib:
            continue
        if "libm" in lib:
            continue
        if "ld-linux" in lib:
            continue
        if "stdc++" in lib:
            continue
        if "libm" in lib:
            continue
        if "libgcc_s" in lib:
            continue
        # OpenMP sometimes links this
        if "libgomp" in lib:
            continue
        print(f"Package '{pkg}': possible wrong linked shared library: {lib}")


LESS_MAGIC = 2
if len(sys.argv) != LESS_MAGIC:
    print("Invalid arguments!")
    sys.exit(1)

store = pathlib.Path(sys.argv[1])

if not (store / "gcc_wrapper").exists():
    print("Sorry, linkcheck currently only supports GCC builds")
    sys.exit(1)

if not store.exists() or not store.is_dir():
    print(f"Invalid store: {store}")

exclude_pkg = [
    "elfutils"  # Elfutils is allergic to correct linking, don't bother with fixing until something actually breaks
]

for path in store.iterdir():
    if path.name in exclude_pkg:
        print(f"Excluding {path.name}, because it is a known brokenly linked package!")
    for file in path.glob("**"):
        if file.is_file(follow_symlinks=False) and file.stat().st_mode & stat.S_IXUSR:
            f = subprocess.run(["ldd", str(file)], check=False, capture_output=True)
            libs = f.stdout.decode()
            libs = libs.split("\n")
            libs.remove("")
            check_libs(path.name, libs)
