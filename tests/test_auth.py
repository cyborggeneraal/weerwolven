from tests import client

def test_read_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {"username":"cyborggeneraal"}