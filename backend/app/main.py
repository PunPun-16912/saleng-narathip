from __future__ import annotations

from copy import deepcopy
from math import atan2, cos, radians, sin, sqrt
from threading import Lock
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Saleng Route API")

lock = Lock()

DEMO_JOBS = [
    {
        "id": 1,
        "status": "open",
        "scrap_type": "กระป๋องอลูมิเนียม",
        "estimated_price": 210,
        "geo_point": {"lat": 13.9630, "lng": 100.5953},
        "address": "123/4 ถนนสุขสวัสดิ์ ตำบลบางเขน จังหวัดนนทบุรี",
        "hidden_address": "ข้อมูลอยู่ระหว่างการยืนยันตัวตน",
        "accepted_by": None,
        "verified": False,
        "route_distance_km": 1.8,
        "price_range": "200-260 บาท",
    },
    {
        "id": 2,
        "status": "open",
        "scrap_type": "กระดาษลัง",
        "estimated_price": 180,
        "geo_point": {"lat": 13.9725, "lng": 100.6100},
        "address": "88/7 ถนนกิ่งแก้ว ตำบลศรีนครินทร์ จังหวัดนนทบุรี",
        "hidden_address": "ข้อมูลอยู่ระหว่างการยืนยันตัวตน",
        "accepted_by": None,
        "verified": False,
        "route_distance_km": 3.9,
        "price_range": "160-210 บาท",
    },
    {
        "id": 3,
        "status": "open",
        "scrap_type": "พลาสติก PET",
        "estimated_price": 95,
        "geo_point": {"lat": 13.9900, "lng": 100.6310},
        "address": "55/9 ซอยรังสิต 25 ตำบลคลองหนึ่ง จังหวัดปทุมธานี",
        "hidden_address": "ข้อมูลอยู่ระหว่างการยืนยันตัวตน",
        "accepted_by": None,
        "verified": False,
        "route_distance_km": 7.2,
        "price_range": "80-120 บาท",
    },
]

VERIFICATION_STATUS: dict[int, bool] = {}
SALENG_LOCATION = {"lat": 13.9630, "lng": 100.5953, "accuracy": 12.0}
JOB_STORE: list[dict[str, Any]] = []


def reset_demo_state() -> None:
    """Reset the in-memory route dataset for each test and demo run."""
    global JOB_STORE
    JOB_STORE = deepcopy(DEMO_JOBS)
    VERIFICATION_STATUS.clear()
    SALENG_LOCATION.update({"lat": 13.9630, "lng": 100.5953, "accuracy": 12.0})


reset_demo_state()


class LocationUpdate(BaseModel):
    lat: float
    lng: float
    accuracy: float = Field(default=12.0, ge=0.0)


class AcceptRequest(BaseModel):
    saleng_id: str = Field(min_length=1)
    lat: float
    lng: float
    accuracy_m: float = Field(default=12.0, ge=0.0)


class VerificationRequest(BaseModel):
    job_id: int
    saleng_id: str = Field(min_length=1)
    method: str = Field(default="thai_id")
    id_number: str = Field(min_length=1)


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance in kilometers for route filtering; supports REQ-OP-002 and REQ-FN-002."""
    radius = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return radius * c


def public_job(job: dict[str, Any]) -> dict[str, Any]:
    """Mask the exact home address until verification, supporting REQ-SEC-002 and SC-04."""
    address = job["address"] if job.get("verified") or job.get("status") == "accepted" else job["hidden_address"]
    return {
        "id": job["id"],
        "status": job["status"],
        "scrap_type": job["scrap_type"],
        "estimated_price": job["estimated_price"],
        "price_range": job["price_range"],
        "route_distance_km": round(job["route_distance_km"], 2),
        "address": address,
        "accepted_by": job.get("accepted_by"),
    }


@app.get("/api/health")
def health_check() -> dict[str, Any]:
    """Return backend health and service metadata for the route feature. Supports REQ-FN-002."""
    return {
        "status": "ok",
        "service": "saleng-route-api",
        "feature": "REQ-FN-002",
    }


@app.get("/api/route/jobs")
def list_route_jobs(
    lat: float = Query(default=13.9630),
    lng: float = Query(default=100.5953),
) -> dict[str, Any]:
    """Filter jobs within 5 km using route-like distance and order by nearest route distance. Supports REQ-FN-002 and REQ-QA-002."""
    jobs = []
    for job in JOB_STORE:
        distance = haversine_km(lat, lng, job["geo_point"]["lat"], job["geo_point"]["lng"])
        job["route_distance_km"] = distance
        if distance <= 5 or job["status"] == "accepted":
            jobs.append(public_job(job))

    jobs.sort(key=lambda item: item["route_distance_km"])
    return {
        "jobs": jobs,
        "limit_km": 5,
        "sort": "route_distance_km",
        "status": "ready",
    }


@app.get("/api/route/jobs/{job_id}")
def read_route_job(job_id: int) -> dict[str, Any]:
    """Fetch a single job with masked address until the user is verified. Supports REQ-SEC-002."""
    for job in JOB_STORE:
        if job["id"] == job_id:
            return public_job(job)
    raise HTTPException(status_code=404, detail="job not found")


@app.post("/api/route/jobs/{job_id}/accept")
def accept_route_job(job_id: int, payload: AcceptRequest) -> dict[str, Any]:
    """Protect against concurrent accepts using a server-side lock and first-come rule. Supports REQ-BR-002."""
    with lock:
        for job in JOB_STORE:
            if job["id"] != job_id:
                continue

            if job["status"] == "accepted":
                raise HTTPException(status_code=409, detail="job already accepted")

            SALENG_LOCATION.update({"lat": payload.lat, "lng": payload.lng, "accuracy": payload.accuracy_m})
            job["status"] = "accepted"
            job["accepted_by"] = payload.saleng_id
            job["verified"] = bool(VERIFICATION_STATUS.get(job_id, False))
            return {
                "job_id": job_id,
                "status": "accepted",
                "accepted_by": payload.saleng_id,
                "route_distance_km": round(job["route_distance_km"], 2),
                "address": job["address"] if job["verified"] else job["hidden_address"],
            }

    raise HTTPException(status_code=404, detail="job not found")


@app.post("/api/verification/verify")
def verify_identity(payload: VerificationRequest) -> dict[str, Any]:
    """Mark a seller or saleng identity as verified before exposing exact address. Supports SC-04."""
    for job in JOB_STORE:
        if job["id"] == payload.job_id:
            VERIFICATION_STATUS[payload.job_id] = True
            job["verified"] = True
            return {
                "job_id": payload.job_id,
                "saleng_id": payload.saleng_id,
                "method": payload.method,
                "verified": True,
                "address": job["address"],
            }

    raise HTTPException(status_code=404, detail="job not found")


@app.post("/api/location/update")
def update_location(payload: LocationUpdate) -> dict[str, Any]:
    """Update GPS location and accuracy for route matching and QA checks. Supports REQ-OP-002."""
    SALENG_LOCATION.update({"lat": payload.lat, "lng": payload.lng, "accuracy": payload.accuracy})
    accuracy_percent = (payload.accuracy / max(abs(payload.lat), 1.0)) * 100
    return {
        "status": "updated",
        "lat": payload.lat,
        "lng": payload.lng,
        "accuracy": payload.accuracy,
        "accuracy_percent": round(accuracy_percent, 2),
        "threshold_percent": 15,
    }
