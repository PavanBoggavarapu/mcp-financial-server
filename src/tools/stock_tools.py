from src.db.client import supabase
from src.utils.errors import NotFoundError


def get_stock_price_history(
    ticker: str,
    start_date: str = None,
    end_date: str = None,
    limit: int = 30
):
    """
    Get historical stock prices for a company
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
        .table("stock_prices")
        .select("*")
        .eq("company_id", company[0]["id"])
    )

    if start_date:
        query = query.gte("date", start_date)

    if end_date:
        query = query.lte("date", end_date)

    data = (
        query
        .order("date", desc=True)
        .limit(limit)
        .execute()
        .data
    )

    if not data:
        raise NotFoundError("No stock price data found")

    return data
