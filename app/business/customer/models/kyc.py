from __future__ import annotations

from dataclasses import dataclass

from app.business.customer.enums.kyc_status import KYCStatus


@dataclass(slots=True)
class KYC:
    verified: bool = False
    status: KYCStatus = KYCStatus.UNKNOWN
    kra_name: str | None = None
    pan_updated: bool = False
    pan_documents_uploaded: bool = False