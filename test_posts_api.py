import pytest

POST_FIELDS = {"userId": int, "id": int, "title": str, "body": str}


def test_list_posts_returns_100_items(api):
    response = api.get("/posts")

    assert response.status_code == 200
    assert len(response.json()) == 100


def test_response_is_json(api):
    response = api.get("/posts/1")

    assert "application/json" in response.headers["Content-Type"]


def test_single_post_has_expected_fields_and_types(api):
    response = api.get("/posts/1")
    post = response.json()

    assert response.status_code == 200
    assert post["id"] == 1
    for field, expected_type in POST_FIELDS.items():
        assert field in post, f"missing field: {field}"
        assert isinstance(post[field], expected_type), f"{field} has wrong type"


def test_missing_post_returns_404(api):
    response = api.get("/posts/99999")

    assert response.status_code == 404


def test_filter_posts_by_user_id(api):
    response = api.get("/posts", params={"userId": 1})
    posts = response.json()

    assert response.status_code == 200
    assert len(posts) == 10
    assert all(post["userId"] == 1 for post in posts)


def test_post_comments_belong_to_post(api):
    response = api.get("/posts/1/comments")
    comments = response.json()

    assert response.status_code == 200
    assert len(comments) == 5
    assert all(comment["postId"] == 1 for comment in comments)
    assert all("@" in comment["email"] for comment in comments)


def test_create_post_echoes_data_and_assigns_id(api):
    payload = {"title": "qa title", "body": "qa body", "userId": 1}

    response = api.post("/posts", json=payload)
    created = response.json()

    assert response.status_code == 201
    assert created["title"] == payload["title"]
    assert created["body"] == payload["body"]
    assert created["userId"] == payload["userId"]
    assert created["id"] == 101  # next id after the 100 existing posts


def test_update_post_with_put(api):
    payload = {"id": 1, "title": "new title", "body": "new body", "userId": 1}

    response = api.put("/posts/1", json=payload)

    assert response.status_code == 200
    assert response.json() == payload


def test_partial_update_with_patch(api):
    response = api.patch("/posts/1", json={"title": "patched title"})
    post = response.json()

    assert response.status_code == 200
    assert post["title"] == "patched title"
    assert post["id"] == 1  # untouched fields are still there


def test_delete_post(api):
    response = api.delete("/posts/1")

    assert response.status_code == 200
    assert response.json() == {}


@pytest.mark.parametrize("user_id", range(1, 11))
def test_each_user_has_name_and_valid_email(api, user_id):
    response = api.get(f"/users/{user_id}")
    user = response.json()

    assert response.status_code == 200
    assert user["id"] == user_id
    assert user["name"]
    assert "@" in user["email"]
