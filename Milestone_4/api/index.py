import sys
import os
import traceback

def get_diag_report():
    info = []
    info.append("=== PYTHON RUNTIME DIAGNOSTIC ===")
    info.append(f"Python Version: {sys.version}")
    info.append(f"CWD: {os.getcwd()}")
    try:
        info.append(f"Files in cwd: {os.listdir('.')}")
    except Exception as e:
        info.append(f"Listdir cwd err: {e}")
    if os.path.exists("/var/task"):
        try:
            info.append(f"Files in /var/task: {os.listdir('/var/task')}")
        except Exception as e:
            info.append(f"Listdir /var/task err: {e}")

    info.append("\n=== DEPENDENCY CHECKS ===")
    for mod in ["fastapi", "pydantic", "sqlalchemy", "jwt", "pandas", "numpy"]:
        try:
            m = __import__(mod)
            info.append(f"  {mod}: OK (version: {getattr(m, '__version__', 'unknown')})")
        except Exception as e:
            info.append(f"  {mod}: FAILED ({e})")

    info.append("\n=== BACKEND IMPORT CHECK ===")
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if BASE_DIR not in sys.path:
        sys.path.insert(0, BASE_DIR)
    milestone4_dir = os.path.join(BASE_DIR, "Milestone_4")
    if os.path.exists(milestone4_dir) and milestone4_dir not in sys.path:
        sys.path.insert(0, milestone4_dir)

    try:
        from backend.main import app as real_fastapi
        info.append(f"  backend.main: OK ({real_fastapi})")
    except Exception as e:
        info.append(f"  backend.main: FAILED:\n{traceback.format_exc()}")

    return "\n".join(info)

# WSGI entrypoint
def app(environ, start_response):
    body = get_diag_report().encode("utf-8")
    start_response("200 OK", [
        ("Content-Type", "text/plain; charset=utf-8"),
        ("Content-Length", str(len(body)))
    ])
    return [body]

# BaseHTTPRequestHandler fallback
from http.server import BaseHTTPRequestHandler
class handler(BaseHTTPRequestHandler):
    def _respond(self):
        body = get_diag_report().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def do_GET(self): self._respond()
    def do_POST(self): self._respond()
    def do_PUT(self): self._respond()
    def do_DELETE(self): self._respond()
    def do_OPTIONS(self): self._respond()
