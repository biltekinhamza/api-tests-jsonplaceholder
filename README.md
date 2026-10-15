# API Tests for JSONPlaceholder (Python + Pytest + Requests)

[![Tests](https://github.com/biltekinhamza/api-tests-jsonplaceholder/actions/workflows/tests.yml/badge.svg)](https://github.com/biltekinhamza/api-tests-jsonplaceholder/actions/workflows/tests.yml)

Automated REST API tests for the free public fake API https://jsonplaceholder.typicode.com.
The same structure works for any JSON REST API: swap the base URL and endpoints.

## What is tested
| Area | Checks |
|---|---|
| `GET /posts` | status code, number of items |
| `GET /posts/1` | JSON content type, required fields and their types |
| `GET /posts/99999` | returns 404 for a missing resource |
| `GET /posts?userId=1` | query-parameter filtering returns only that user's posts |
| `GET /posts/1/comments` | nested resource belongs to the post, emails look valid |
| `POST /posts` | returns 201, echoes the sent data, assigns a new id |
| `PUT /posts/1` | returns 200 with the full updated resource |
| `PATCH /posts/1` | partial update keeps untouched fields |
| `DELETE /posts/1` | returns 200 and an empty object |
| `GET /users/{1..10}` | parametrized test: every user has a name and a valid email |

20 test cases in total.

## Setup
```
python -m venv .venv
# Windows: .venv\Scripts\activate    Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## Run
```
pytest -v
pytest --html=report.html --self-contained-html   # HTML report
```

## Project structure
- `conftest.py` – `ApiClient` wrapper (base URL, timeout, shared session) and the `api` fixture
- `test_posts_api.py` – the test cases
- `.github/workflows/tests.yml` – runs the suite on every push; the HTML report is attached to each run

## Notes
JSONPlaceholder is a fake API: write requests (POST/PUT/PATCH/DELETE) return realistic
responses but do not change the stored data, so the tests can run repeatedly.
