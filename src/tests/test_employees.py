import json

import pytest

from app.api import crud


def test_create_note(test_app, monkeypatch):
    test_request_payload = {"name": "something", "second_name": "something else", "salary": 1000}
    test_response_payload = {"id": 1, "name": "something", "second_name": "something else", "salary": 1000}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post("/employees/", data=json.dumps(test_request_payload),)

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_note_invalid_json(test_app):
    response = test_app.post("/employees/", data=json.dumps({"name": "something"}))
    assert response.status_code == 422

    response = test_app.post("/employees/", data=json.dumps({"second_name": "something else"}))
    assert response.status_code == 422

    response = test_app.post("/employees/", data=json.dumps({"salary": "something"}))
    assert response.status_code == 422

    response = test_app.post("/employees/", data=json.dumps({"name": "something", "second_name": "something else",
                                                             "salary": 0}))
    assert response.status_code == 422

    response = test_app.post("/employees/", data=json.dumps({"name": "something", "second_name": "something else",
                                                             "salary": 1000001}))
    assert response.status_code == 422

    response = test_app.post("/employees/", data=json.dumps({"name": "1", "second_name": "2"}))
    assert response.status_code == 422


def test_read_note(test_app, monkeypatch):
    test_data = {"id": 1, "name": "something", "second_name": "something else", "salary": 1000}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/employees/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_note_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/employees/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

    response = test_app.get("/employees/0")
    assert response.status_code == 422


def test_read_all_notes(test_app, monkeypatch):
    test_data = [
        {"name": "something", "second_name": "something else", "salary": 1000, "id": 1},
        {"name": "someone", "second_name": "someone else", "salary": 1000, "id": 2},
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/employees/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_update_note(test_app, monkeypatch):
    test_update_data = {"name": "someone", "second_name": "someone else", "salary": 1000, "id": 1}

    async def mock_get(id):
        return True

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put("/employees/1/", data=json.dumps(test_update_data))
    assert response.status_code == 200
    assert response.json() == test_update_data


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"second_name": "bar"}, 422],
        [999, {"name": "foo", "second_name": "bar", "salary": 1000}, 404],
        [1, {"name": "1", "last_name": "bar", "salary": 1000}, 422],
        [1, {"name": "foo", "last_name": "bar", "salary": "seven"}, 422],
        [1, {"name": "foo", "second_name": "1", "salary": 1000}, 422],
        [0, {"name": "foo", "second_name": "bar", "salary": 1000}, 422],
    ],
)
def test_update_note_invalid(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.put(f"/employees/{id}/", data=json.dumps(payload),)
    assert response.status_code == status_code


def test_remove_note(test_app, monkeypatch):
    test_data = {"name": "something", "second_name": "something else", "salary": 1000, "id": 1}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete("/employees/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_note_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete("/employees/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

    response = test_app.delete("/employees/0/")
    assert response.status_code == 422



