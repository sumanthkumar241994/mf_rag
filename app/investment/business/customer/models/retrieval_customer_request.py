from app.investment.base.models import RequestContext
from app.investment.business.base.model import BusinessBaseModel


class RetrieveCustomerRequest(BusinessBaseModel):
    request: RequestContext