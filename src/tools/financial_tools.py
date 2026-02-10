from src.db.client import supabase
from src.utils.errors import NotFoundError


def get_financial_report(
    ticker: str,
    fiscal_year: int = None,
    fiscal_quarter: str = None
):
    """
    Get quarterly or annual financial reports for a company
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
        .table("financial_reports")
        .select("*")
        .eq("company_id", company[0]["id"])
    )

    if fiscal_year:
        query = query.eq("fiscal_year", fiscal_year)

    if fiscal_quarter:
        query = query.eq("fiscal_quarter", fiscal_quarter)

    data = query.order("report_date", desc=True).execute().data

    if not data:
        raise NotFoundError("No financial reports found")

    return data


def compare_companies(tickers: list, metrics: list = None):
    """
    Compare 2–5 companies side-by-side on key financial metrics
    """
    if not metrics:
        metrics = ["revenue", "net_income", "eps", "gross_margin"]

    companies = (
        supabase
        .table("companies")
        .select("id, ticker, name")
        .in_("ticker", tickers)
        .execute()
        .data
    )

    if not companies:
        raise NotFoundError("No companies found")

    company_map = {c["id"]: c for c in companies}

    reports = (
        supabase
        .table("financial_reports")
        .select("company_id," + ",".join(metrics))
        .in_("company_id", list(company_map.keys()))
        .order("report_date", desc=True)
        .execute()
        .data
    )

    if not reports:
        raise NotFoundError("No financial data available for comparison")

    result = {}
    for r in reports:
        ticker = company_map[r["company_id"]]["ticker"]
        result.setdefault(ticker, []).append(r)

    return result


def screen_stocks(
    min_revenue: float = None,
    min_eps: float = None,
    min_gross_margin: float = None,
    max_debt_to_equity: float = None,
    sector: str = None
):
    """
    Screen stocks based on financial criteria
    """
    query = (
        supabase
        .table("financial_reports")
        .select(
            "revenue, eps, gross_margin, debt_to_equity, company_id, companies(ticker, sector)"
        )
        .order("report_date", desc=True)
    )

    if min_revenue:
        query = query.gte("revenue", min_revenue)

    if min_eps:
        query = query.gte("eps", min_eps)

    if min_gross_margin:
        query = query.gte("gross_margin", min_gross_margin)

    if max_debt_to_equity:
        query = query.lte("debt_to_equity", max_debt_to_equity)

    data = query.execute().data

    if sector:
        data = [d for d in data if d["companies"]["sector"] == sector]

    if not data:
        raise NotFoundError("No stocks match screening criteria")

    return data
