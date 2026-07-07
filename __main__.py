'''
Lets the tool run as a module:  python -m aie  (when the project
directory is named/installed as "aie") or  python .  from the repo root.
'''

import sys

from cli import main

if __name__ == "__main__":
    sys.exit(main())
