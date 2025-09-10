from typing import List, Optional
from pydantic import BaseModel

class FilterCriteria(BaseModel):
    status: Optional[str] = None
    assigned_to: Optional[int] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None

class Deal(BaseModel):
    id: int
    name: str
    status: str
    value: float
    assigned_to: int

deals_db = [
    {"id": 1, "name": "Deal 1", "status": "open", "value": 1000, "assigned_to": 1},
    {"id": 2, "name": "Deal 2", "status": "closed", "value": 2000, "assigned_to": 2},
    {"id": 3, "name": "Deal 3", "status": "open", "value": 1500, "assigned_to": 1},
]

def filter_deals(criteria: FilterCriteria) -> List[Deal]:
    filtered = deals_db
    if criteria.status:
        filtered = [d for d in filtered if d["status"] == criteria.status]
    if criteria.assigned_to:
        filtered = [d for d in filtered if d["assigned_to"] == criteria.assigned_to]
    if criteria.min_value:
        filtered = [d for d in filtered if d["value"] >= criteria.min_value]
    if criteria.max_value:
        filtered = [d for d in filtered if d["value"] <= criteria.max_value]
    return filtered
