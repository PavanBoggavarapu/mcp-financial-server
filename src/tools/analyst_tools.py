from src.db.client import supabase
from src.utils.errors import NotFoundError


def get_analyst_ratings(ticker: str, firm: str = None):
    """
    Get latest analyst ratings for a company
    """
    company = (
        supabase
        .table("companies")
        .select("id")
        .eq("ticker", ticker)
        .limit(1)
        .execute()
        .data
    )

    if not company:
        raise NotFoundError(f"Company not found: {ticker}")

    query = (
        supabase
        .table("analyst_ratings")
        .select("*")
        .eq("company_id", company[0]["id"])
    )

    if firm:
        query = query.ilike("analyst_firm", f"%{firm}%")

    data = (
        query
        .order("rating_date", desc=True)
        .limit(10)
        .execute()
        .data
    )

    if not data:
        raise NotFoundError("No analyst ratings found")

    return data
