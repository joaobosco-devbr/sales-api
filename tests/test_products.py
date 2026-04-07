import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlmodel import SQLModel, create_engine
from app.database import DATABASE_URL

TEST_DB = "sqlite:///./test.db"

client = TestClient(app)

@pytest.fixture(autouse=True, scope='session')
def prepare_db():
    os.environ['DATABASE_URL'] = TEST_DB
    engine = create_engine(TEST_DB, echo=False)
    SQLModel.metadata.create_all(engine)
    yield
    try:
        os.remove("./test.db")
    except:
        pass

def test_signup_and_product_crud():
    # signup returns 201
    r = client.post("/signup", json={"username": "testuser", "password": "secret"})
    assert r.status_code == 201

    # get token
    r = client.post("/token", data={"username": "testuser", "password": "secret"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # create product
    payload = {"name": "Caneca", "description": "Caneca linda", "price": 25.0, "stock": 10}
    r = client.post("/products", json=payload, headers=headers)
    assert r.status_code == 201
    pid = r.json()["id"]

    # list products
    r = client.get("/products")
    assert r.status_code == 200
    assert any(p["id"] == pid for p in r.json())

    # get product by id
    r = client.get(f"/products/{pid}")
    assert r.status_code == 200
    assert r.json()["name"] == "Caneca"

    # update product
    r = client.put(f"/products/{pid}", json={"name": "Caneca XL", "price": 30.0, "stock": 5}, headers=headers)
    assert r.status_code == 200
    assert r.json()["name"] == "Caneca XL"

    # place order
    r = client.post("/orders", json={"items": [{"product_id": pid, "quantity": 2}]}, headers=headers)
    assert r.status_code == 201
    oid = r.json()["id"]
    assert r.json()["total"] == 60.0

    # get order
    r = client.get(f"/orders/{oid}", headers=headers)
    assert r.status_code == 200

    # delete product
    r = client.delete(f"/products/{pid}", headers=headers)
    assert r.status_code == 204
