from app import app

def test_home_route_status_code():
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
