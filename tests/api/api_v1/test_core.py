from fastapi.testclient import TestClient


def test_home(client: TestClient) -> None:
    r = client.get("/")
    assert 200 <= r.status_code < 300
    version_info = r.json()
    for info in ["application", "python", "fastapi", "pydantic"]:
        assert info in version_info


def test_version(client: TestClient) -> None:
    r = client.get("/version")
    assert 200 <= r.status_code < 300
    version_info = r.json()
    for info in ["application", "python", "fastapi", "pydantic"]:
        assert info in version_info
