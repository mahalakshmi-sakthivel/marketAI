import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Vercel's Python runtime serves this ASGI app directly.
from backend.main import app  # noqa: E402,F401
