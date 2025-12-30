import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlmodel import SQLModel, create_engine
from app.database import DATABASE_URL

# For tests we prefer a sqlite file to run quickly
TEST_DB = "sqlite:///./test.db"

client = TestClient(app)

@pytest.fixture(autouse=True, scope='session')
def prepare_db():
    # ensure using sqlite for tests to avoid requiring mysql in CI local
    os.environ['DATABASE_URL'] = TEST_DB
    engine = create_engine(TEST_DB, echo=False)
    SQLModel.metadata.create_all(engine)
    yield
    # cleanup file after tests (optional)
    try:
        os.remove("./test.db")
    except:
        pass

@pytest.mark.integration
def test_signup_and_product_crud():

    # signup
    r = client.post("/signup", json={"username":"testuser","password":"secret"})
    assert r.status_code == 200
    # get token
    r = client.post("/token", data={"username":"testuser","password":"secret"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # create product
    payload = {"name":"Caneca", "description":"Caneca linda", "price":25.0, "stock":10}
    r = client.post("/products", json=payload, headers=headers)
    assert r.status_code == 200
    pid = r.json()["id"]

    # get product
    r = client.get(f"/products/{pid}")
    assert r.status_code == 200
    assert r.json()["name"] == "Caneca"
