from tests.conftest import login

LUNCH = {"title": "Team lunch", "amount": 850, "category": "food", "spent_on": "2026-11-01"}


def test_create_expense(client, auth):
    res = client.post("/expenses", json=LUNCH, headers=auth)
    assert res.status_code == 201
    body = res.json()
    assert body["id"] == 1
    assert body["title"] == "Team lunch"
    assert "owner_id" not in body  # hidden by the response model


def test_invalid_expense_is_rejected(client, auth):
    res = client.post("/expenses", json={**LUNCH, "amount": -50}, headers=auth)
    assert res.status_code == 422
    assert res.json()["detail"][0]["loc"] == ["body", "amount"]


def test_list_and_filter(client, auth):
    client.post("/expenses", json=LUNCH, headers=auth)
    client.post("/expenses", json={"title": "Metro card", "amount": 500, "category": "travel"}, headers=auth)
    assert len(client.get("/expenses", headers=auth).json()) == 2
    travel = client.get("/expenses?category=travel", headers=auth).json()
    assert [e["title"] for e in travel] == ["Metro card"]


def test_summary(client, auth):
    client.post("/expenses", json=LUNCH, headers=auth)
    client.post("/expenses", json={**LUNCH, "amount": 150}, headers=auth)
    client.post(
        "/expenses", json={"title": "Electricity", "amount": 1999.5, "category": "bills"}, headers=auth
    )
    summary = client.get("/expenses/summary", headers=auth).json()
    assert summary == {"total": 2999.5, "by_category": {"food": 1000, "bills": 1999.5}}


def test_update_and_delete(client, auth):
    expense_id = client.post("/expenses", json=LUNCH, headers=auth).json()["id"]
    res = client.patch(f"/expenses/{expense_id}", json={"amount": 900}, headers=auth)
    assert res.json()["amount"] == 900
    assert res.json()["title"] == "Team lunch"  # fields we didn't send stay the same

    assert client.delete(f"/expenses/{expense_id}", headers=auth).status_code == 204
    assert client.get(f"/expenses/{expense_id}", headers=auth).status_code == 404


def test_users_only_see_their_own_expenses(client, auth):
    expense_id = client.post("/expenses", json=LUNCH, headers=auth).json()["id"]
    other = login(client, username="ravi")
    assert client.get(f"/expenses/{expense_id}", headers=other).status_code == 404
    assert client.get("/expenses", headers=other).json() == []
