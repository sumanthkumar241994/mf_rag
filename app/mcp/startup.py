# app/mcp/startup.py

from app.business.customer.customer_service import CustomerService
from fastmcp import FastMCP

from app.mcp.tools.customer import register_customer_tools


def register_mcp_tools(
    mcp: FastMCP,
    customer_service: CustomerService,
) -> None:

    register_customer_tools(
        mcp=mcp,
        customer_service=customer_service,
    )