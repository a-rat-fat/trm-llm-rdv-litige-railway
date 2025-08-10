
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
import json, os, datetime

router = APIRouter()
DATA_PATH = os.environ.get("DATA_PATH", "/app/data")

class RDVRequest(BaseModel):
    client_id: str
    site_id: str
    desired_date: str  # ISO date
    window: Optional[str] = None  # "AM", "PM", "FULL"
    duration_min: int = 30
    vehicle_type: Optional[str] = "TRR"
    constraints: Optional[List[str]] = None
    notes: Optional[str] = None

class RDVProposal(BaseModel):
    slot_start: str
    slot_end: str
    confidence: float
    rationale: str

@router.post("/suggest_slots", response_model=List[RDVProposal])
def suggest_slots(req: RDVRequest):
    sites = json.load(open(os.path.join(DATA_PATH, "sites.json"), encoding="utf-8"))
    site = next((s for s in sites if s["id"] == req.site_id), None)
    if not site:
        return []
    desired = datetime.datetime.fromisoformat(req.desired_date)
    weekday = desired.weekday()
    if weekday in site.get("blackout_weekdays", []):
        return []
    slots = []
    windows = {
        "AM": [(8,0, 12,0)],
        "PM": [(13,30, 17,0)],
        "FULL": [(8,0, 12,0), (13,30, 17,0)],
        None: [(8,0, 12,0), (13,30, 17,0)]
    }[req.window]
    for (h1,m1,h2,m2) in windows:
        start = desired.replace(hour=h1, minute=m1, second=0, microsecond=0)
        end   = desired.replace(hour=h2, minute=m2, second=0, microsecond=0)
        current = start
        while current + datetime.timedelta(minutes=req.duration_min) <= end:
            slot_end = current + datetime.timedelta(minutes=req.duration_min)
            slots.append(RDVProposal(
                slot_start=current.isoformat(),
                slot_end=slot_end.isoformat(),
                confidence=0.6,
                rationale="Capacité standard, pas de conflit connu (MVP)"
            ))
            current += datetime.timedelta(minutes=req.duration_min)
    return slots[:12]
