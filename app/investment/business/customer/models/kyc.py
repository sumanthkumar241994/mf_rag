

from app.investment.base.models import InvestmentBaseModel
from app.investment.business.customer.enums.kyc_status import KYCStatus


class KYC(InvestmentBaseModel):
    verified: bool = False
    status: KYCStatus = KYCStatus.UNKNOWN
    kra_name: str | None = None
    pan_updated: bool = False
    pan_documents_uploaded: bool = False