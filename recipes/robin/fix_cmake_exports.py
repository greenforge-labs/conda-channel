"""Fix robin's cmake export files by removing build-tree paths.

Robin's CMakeLists.txt leaks BUILD_INTERFACE paths into installed cmake
config files. This script strips any absolute path that doesn't start
with the install prefix from INTERFACE_INCLUDE_DIRECTORIES.
"""

import glob
import os
import re
import sys

prefix = sys.argv[1]
cmake_dir = os.path.join(prefix, "lib", "cmake")

if not os.path.isdir(cmake_dir):
    print(f"No cmake dir at {cmake_dir}, nothing to fix")
    sys.exit(0)

for cmake_file in glob.glob(os.path.join(cmake_dir, "**", "*.cmake"), recursive=True):
    with open(cmake_file, "r") as f:
        content = f.read()

    original = content

    def fix_line(match):
        line = match.group(0)
        paths_match = re.search(r'"([^"]*)"', line)
        if not paths_match:
            return line
        paths_str = paths_match.group(1)
        paths = [p.strip() for p in paths_str.split(";") if p.strip()]
        kept = []
        for p in paths:
            # Keep: generator expressions, relative paths, paths under prefix
            if p.startswith("$") or p.startswith("${") or not os.path.isabs(p):
                kept.append(p)
            elif p.startswith(prefix):
                kept.append(p)
            else:
                print(f"  Removing build-tree path: {p}")
        if kept == paths:
            return line
        return line[: paths_match.start(1)] + ";".join(kept) + line[paths_match.end(1) :]

    content = re.sub(
        r'.*INTERFACE_INCLUDE_DIRECTORIES.*"[^"]*".*',
        fix_line,
        content,
    )

    if content != original:
        print(f"Fixed: {cmake_file}")
        with open(cmake_file, "w") as f:
            f.write(content)
