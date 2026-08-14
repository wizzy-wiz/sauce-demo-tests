"""API test suite against https://jsonplaceholder.typicode.com — a free,
public fake REST API with no signup or API key required. Widely used for
practicing and demonstrating API-level testing.

Demonstrates automated testing at the API layer, separate from the UI-layer
tests in tests/. No browser required — these run against raw HTTP requests.
"""

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


def test_get_single_post_returns_200_and_correct_id():
    response = requests.get(f"{BASE_URL}/posts/1")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert "title" in body
    assert "userId" in body


def test_get_nonexistent_post_returns_404():
    response = requests.get(f"{BASE_URL}/posts/9999")

    assert response.status_code == 404


def test_list_posts_returns_all_entries():
    response = requests.get(f"{BASE_URL}/posts")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 100
    assert all("title" in post for post in body)


def test_filter_posts_by_user_id():
    response = requests.get(f"{BASE_URL}/posts", params={"userId": 1})

    assert response.status_code == 200
    body = response.json()
    assert len(body) > 0
    assert all(post["userId"] == 1 for post in body)


def test_create_post_returns_201_with_submitted_data():
    payload = {
        "title": "Test Automation Engineer role",
        "body": "Automated API test verifying resource creation.",
        "userId": 1,
    }
    response = requests.post(f"{BASE_URL}/posts", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == payload["title"]
    assert body["userId"] == payload["userId"]
    assert "id" in body


def test_update_post_returns_200_with_updated_data():
    payload = {"title": "Updated title"}
    response = requests.patch(f"{BASE_URL}/posts/1", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == payload["title"]


def test_delete_post_returns_200():
    response = requests.delete(f"{BASE_URL}/posts/1")

    assert response.status_code == 200


def test_get_comments_for_a_post():
    response = requests.get(f"{BASE_URL}/posts/1/comments")

    assert response.status_code == 200
    body = response.json()
    assert len(body) > 0
    assert all(comment["postId"] == 1 for comment in body)
