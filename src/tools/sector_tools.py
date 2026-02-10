from src.db.client import supabase
from src.utils.errors import NotFoundError


def get_sector_overview(sector: str):
    """
    Get aggregated statistics for a sector
    """
    companies = (
        supabase
        .table("companies")
        .select("id, market_cap")
        .eq("sector", sector)
        .execute()
        .data
    )

    if not companies:
        raise NotFoundError(f"No companies found for sector: {sector}")

    company_ids = [c["id"] for c in companies]
    avg_market_cap = sum(c["market_cap"] for c in companies) / len(companies)

    reports = (
        supabase
        .table("financial_reports")
        .select("gross_margin, operating_margin, company_id")
        .in_("company_id", company_ids)
        .execute()
        .data
    )

    if not reports:
        raise NotFoundError("No financial data found for sector")

    avg_gross_margin = sum(r["gross_margin"] for r in reports) / len(reports)
    avg_operating_margin = sum(r["operating_margin"] for r in reports) / len(reports)

    return {
        "sector": sector,
        "company_count": len(companies),
        "average_market_cap": round(avg_market_cap, 2),
        "average_gross_margin": round(avg_gross_margin, 2),
        "average_operating_margin": round(avg_operating_margin, 2)
    }
