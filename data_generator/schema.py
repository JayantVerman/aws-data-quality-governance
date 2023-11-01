"""Data schema models for synthetic customer dataset."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class CustomerRecord:
    customer_id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    zip: str
    ssn: str
    age: int
    account_balance: float
    credit_score: int
    signup_date: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
