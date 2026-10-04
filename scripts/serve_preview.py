"""Serve the workspace preview on loopback only. No dependencies."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import os

os.chdir(Path(__file__).resolve().parents[1])
ThreadingHTTPServer(("127.0.0.1", 8765), SimpleHTTPRequestHandler).serve_forever()
