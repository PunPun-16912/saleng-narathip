from fastapi.testclient import TestClient

from backend.app.main import app, reset_demo_state

client = TestClient(app)


def test_AC_04_01_route_jobs_visible_within_5km() -> None:
    reset_demo_state()
    response = client.get('/api/route/jobs?lat=13.9630&lng=100.5953')
    assert response.status_code == 200
    payload = response.json()
    assert payload['limit_km'] == 5
    jobs = payload['jobs']
    assert [job['id'] for job in jobs] == [1, 2, 3]
    assert all(job['route_distance_km'] <= 5 for job in jobs)


def test_AC_04_02_route_sorting_by_distance() -> None:
    reset_demo_state()
    response = client.get('/api/route/jobs?lat=13.9630&lng=100.5953')
    payload = response.json()['jobs']
    distances = [job['route_distance_km'] for job in payload]
    assert distances == sorted(distances)


def test_AC_04_05_single_assignee_guard() -> None:
    reset_demo_state()
    first = client.post(
        '/api/route/jobs/1/accept',
        json={'saleng_id': 'saleng-a', 'lat': 13.9630, 'lng': 100.5953, 'accuracy_m': 12},
    )
    second = client.post(
        '/api/route/jobs/1/accept',
        json={'saleng_id': 'saleng-b', 'lat': 13.9630, 'lng': 100.5953, 'accuracy_m': 12},
    )

    assert first.status_code == 200
    assert second.status_code == 409
    assert second.json()['detail'] == 'job already accepted'


def test_AC_04_06_gps_accuracy_threshold() -> None:
    reset_demo_state()
    response = client.post(
        '/api/location/update',
        json={'lat': 13.9630, 'lng': 100.5953, 'accuracy': 10.0},
    )
    assert response.status_code == 200
    assert response.json()['threshold_percent'] == 15
    assert response.json()['accuracy'] <= 15


def test_AC_04_08_address_hidden_until_verified() -> None:
    reset_demo_state()
    response = client.get('/api/route/jobs/1')
    payload = response.json()
    assert 'ข้อมูลอยู่ระหว่างการยืนยันตัวตน' in payload['address']

    verify = client.post(
        '/api/verification/verify',
        json={'job_id': 1, 'saleng_id': 'saleng-a', 'method': 'thai_id', 'id_number': '1234567890123'},
    )
    assert verify.status_code == 200

    released = client.get('/api/route/jobs/1')
    assert released.status_code == 200
    assert released.json()['address'] == '123/4 ถนนสุขสวัสดิ์ ตำบลบางเขน จังหวัดนนทบุรี'
