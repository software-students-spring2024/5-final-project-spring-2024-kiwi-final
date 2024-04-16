import pytest
import openai
from flask import Flask
from mongomock import MongoClient
from unittest.mock import patch
from app2 import create_app, get_key, init_app


def test_sanity_check():
    expected = True  # the value we expect to be present
    actual = True  # the value we see in reality
    assert actual == expected, "Expected True to be equal to True!"

def test_get_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "mock key")
    assert get_key() == "mock key"

@pytest.fixture
def db():
    client = MongoClient()
    db = client.db.collection
    yield db
    client.drop_database(db)

def test_init_app(db, monkeypatch):
    user_data = {
        "name": "Test User",
        "latitude": 40,
        "longitude": -74,
        "city": "New York",
        "region": "New York",
        "country": "United States of America",
        "ml_response": "",
    }
    db.insert_one(user_data)
    monkeypatch.setattr("app.get_key", lambda: "mock key")
    def mock_predict(user_loc, openai_key):
        return "Mock ML Response"
    monkeypatch.setattr("app.predict", mock_predict)
    with patch('flask.Flask.run') as mock_run:
        init_app(db)
    mock_run.assert_called_once_with(host="0.0.0.0", port=5001)

def test_ML_client(db, monkeypatch):
    user_data = {
        "name": "Test User",
        "latitude": 40,
        "longitude": -74,
        "city": "New York",
        "region": "New York",
        "country": "United States of America",
        "ml_response": "",
    }
    db.insert_one(user_data)
    def mock_predict(user_loc, openai_key):
        return "Mock ML Response"
    monkeypatch.setattr("app.predict", mock_predict)
    app = create_app(db, "mock key")
    app.config["TESTING"] = True
    client = app.test_client()
    response = client.get("/ml_result")
    assert response.status_code == 200


def test_ML_client_fail(db, monkeypatch):
    user_data = {
        "name": "Test",
        "latitude": 40,
        "longitude": -74,
        "city": "New York",
        "region": "New York",
        "country": "United States of America",
        "ml_response": "",
    }
    db.insert_one(user_data)
    def mock_predict(user_loc, openai_key):
        return "Mock ML Response"
    monkeypatch.setattr("app.predict", mock_predict)
    app = create_app(db, "mock key")
    app.config["TESTING"] = True
    client = app.test_client()
    response = client.get("/ml_result")
    assert response.status_code == 404
