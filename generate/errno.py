#!/usr/bin/env python
# Usage:
# errno.py path/to/linux/include/uapi/asm-generic/errno{-base,}.h > src/sys/linux/errno.rs
from __future__ import print_function

from collections import namedtuple
import re
DEFINE_REGEX=re.compile(r"^#define\s+(?P<name>E[A-Z0-9]+)\s+(?P<value>\w+)\s*(\/\* (?P<comment>.*) \*\/\s*)?$")

ErrnoValue = namedtuple('ErrnoValue', 'name value comment')

def parse_line(line):
    m = DEFINE_REGEX.match(line)
    if m:
        return ErrnoValue(**m.groupdict())

def main():
    import fileinput
    errno_values = [parse_line(line) for line in fileinput.input()]
    errno_values = [v for v in errno_values if v is not None]
    print("#![allow(dead_code)]")
    print("use ctypes::c_int;");
    print()
    for v in errno_values:
        print("pub const {name}: c_int = {value};".format(**v._asdict()))
    print()
    print("pub fn error_string(errno: i32) -> Option<&'static str> {")
    print("    Some(match errno {")
    for v in errno_values:
        try:
            int(v.value)
        except ValueError:
            continue
        print("        {name} => \"{comment}\",".format(**v._asdict()))
    print("        _ => return None,")
    print("    })")
    print("}")


if __name__ == '__main__':
    main()
