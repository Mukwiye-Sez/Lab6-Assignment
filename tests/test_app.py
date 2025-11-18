import os
import sys

# Add project root (where app.py lives) to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import app  # now this should work


def test_index_status_code():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_index_response_body():
    client = app.test_client()
    response = client.get("/")
    assert b"Hello from Lab 6 pipeline v2 - rolling update!" in response.data