# Pytest configuration to ensure src is on sys.path for imports
import sys
import os

ROOT = os.path.dirname(__file__)
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)
