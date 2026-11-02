def test_health(client):
    assert client.get("/health").json()["status"] == "ok"


def test_register_and_login(client):
    res = client.post("/auth/register", json={"username": "asha", "password": "secret-pass-123"})
    assert res.status_code == 201
    assert res.json() == {"id": 1, "username": "asha"}  # the password hash is never returned

    res = client.post("/auth/token", data={"username": "asha", "password": "secret-pass-123"})
    assert res.status_code == 200
    token = res.json()["access_token"]
    me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.json()["username"] == "asha"


def test_duplicate_username(client):
    client.post("/auth/register", json={"username": "asha", "password": "secret-pass-123"})
    res = client.post("/auth/register", json={"username": "asha", "password": "another-pass-456"})
    assert res.status_code == 409


def test_short_password_is_rejected(client):
    res = client.post("/auth/register", json={"username": "asha", "password": "123"})
    assert res.status_code == 422


def test_wrong_password(client):
    client.post("/auth/register", json={"username": "asha", "password": "secret-pass-123"})
    res = client.post("/auth/token", data={"username": "asha", "password": "wrong-password"})
    assert res.status_code == 401


def test_protected_route_needs_a_token(client):
    assert client.get("/expenses").status_code == 401
    assert client.get("/expenses", headers={"Authorization": "Bearer not-a-real-token"}).status_code == 401
