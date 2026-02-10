from src.db.client import supabase
from src.utils.errors import NotFoundError

from src.db.client import supabase
from src.utils.errors import NotFoundError


def get_company_by_identifier(identifier: str):
    """
    Fetch a company profile by ticker or partial company name
    """
    response = (
        supabase
        .table("companies")
        .select("*")
        .or_(f"ticker.ilike.%{identifier}%,name.ilike.%{identifier}%")
        .limit(1)
        .execute()
    )

    if not response.data:
        raise NotFoundError(f"Company not found: {identifier}")

    return response.data[0]


def search_companies(filters: dict):
    """
    Search companies using multiple filters
    """
    query = supabase.table("companies").select("*")

    if filters.get("sector"):
        query = query.eq("sector", filters["sector"])

    if filters.get("industry"):
        query = query.eq("industry", filters["industry"])

    if filters.get("country"):
        query = query.eq("country", filters["country"])

    if filters.get("min_market_cap"):
        query = query.gte("market_cap", filters["min_market_cap"])

    if filters.get("max_market_cap"):
        query = query.lte("market_cap", filters["max_market_cap"])

    return query.limit(20).execute().data
