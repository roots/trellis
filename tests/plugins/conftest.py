import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# The callback plugin lives under lib/ and is normally picked up by Ansible
# through the callback_plugins path in ansible.cfg. Import it as a package.
LIB_DIR = str(REPO_ROOT / "lib")
if LIB_DIR not in sys.path:
    sys.path.insert(0, LIB_DIR)
