
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import json, os
from jinja2 import Template

router = APIRouter()
DATA_PATH = os.environ.get("DATA_PATH", "/app/data")

class LitigeInput(BaseModel):
    type: str
    client_id: str
    order_ref: str
    site_id: Optional[str] = None
    eta_real: Optional[str] = None
    eta_expected: Optional[str] = None
    photos: Optional[list[str]] = None
    details: Optional[str] = None
    amount_estimated_eur: Optional[float] = None
    contact_email: Optional[str] = None

class LitigeDraft(BaseModel):
    subject: str
    body_html: str
    body_text: str
    suggested_actions: list[str]

@router.post("/draft_email", response_model=LitigeDraft)
def draft_email(inp: LitigeInput):
    clients = json.load(open(os.path.join(DATA_PATH, "clients.json"), encoding="utf-8"))
    client = next((c for c in clients if c["id"] == inp.client_id), None)
    client_name = client["name"] if client else "Client"

    template_html = open(os.path.join(DATA_PATH, "templates", "litige_email.html"), encoding="utf-8").read()
    template_txt  = open(os.path.join(DATA_PATH, "templates", "litige_email.txt"), encoding="utf-8").read()
    subject = f"{client_name} - Dossier litige {inp.type.upper()} - Réf {inp.order_ref}"

    context = {
        "type": inp.type,
        "client_name": client_name,
        "order_ref": inp.order_ref,
        "eta_real": inp.eta_real or "n.c.",
        "eta_expected": inp.eta_expected or "n.c.",
        "details": inp.details or "—",
        "amount_estimated_eur": f"{inp.amount_estimated_eur:.2f} €" if inp.amount_estimated_eur else "n.c.",
        "contact_email": inp.contact_email or (client.get("contact_email") if client else "n.c."),
        "actions": [
            "Accuser réception et ouvrir dossier interne",
            "Analyser preuves (CMR, photos, géoloc véhicule)",
            "Proposer geste commercial si responsabilité avérée",
            "Informer client de l’avancement sous 24–48h"
        ]
    }
    body_html = Template(template_html).render(**context)
    body_text = Template(template_txt).render(**context)
    return LitigeDraft(subject=subject, body_html=body_html, body_text=body_text, suggested_actions=context["actions"])
