from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_backend_health_endpoint() -> None:
    response = client.get('/api/health')
    assert response.status_code == 200
    payload = response.json()
    assert payload['status'] == 'ok'
    assert payload['service'] == 'saleng-route-api'


def test_route_jobs_endpoint_contract() -> None:
    response = client.get('/api/route/jobs')
    assert response.status_code == 200
    payload = response.json()
    assert payload['limit_km'] == 5
    assert payload['sort'] == 'route_distance_km'
    assert 'jobs' in payload
