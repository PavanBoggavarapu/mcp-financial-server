from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.company_tools import (
    get_company_by_identifier,
    search_companies
)
from src.tools.financial_tools import (
    get_financial_report,
    compare_companies,
    screen_stocks
)
from src.tools.stock_tools import get_stock_price_history
from src.tools.analyst_tools import get_analyst_ratings
from src.tools.sector_tools import get_sector_overview

# Create MCP server
server = Server("financial-mcp-server")


def call_tool(name: str, arguments: dict):
    """
    MCP tool dispatcher
    """

    if name == "get_company_profile":
        return get_company_by_identifier(arguments["identifier"])

    elif name == "search_companies":
        return search_companies(arguments)

    elif name == "get_financial_report":
        return get_financial_report(
            ticker=arguments["ticker"],
            fiscal_year=arguments.get("fiscal_year"),
            fiscal_quarter=arguments.get("fiscal_quarter")
        )

    elif name == "compare_companies":
        return compare_companies(
            tickers=arguments["tickers"],
            metrics=arguments.get("metrics")
        )

    elif name == "get_stock_price_history":
        return get_stock_price_history(
            ticker=arguments["ticker"],
            start_date=arguments.get("start_date"),
            end_date=arguments.get("end_date"),
            limit=arguments.get("limit", 30)
        )

    elif name == "get_analyst_ratings":
        return get_analyst_ratings(
            ticker=arguments["ticker"],
            firm=arguments.get("firm")
        )

    elif name == "screen_stocks":
        return screen_stocks(
            min_revenue=arguments.get("min_revenue"),
            min_eps=arguments.get("min_eps"),
            min_gross_margin=arguments.get("min_gross_margin"),
            max_debt_to_equity=arguments.get("max_debt_to_equity"),
            sector=arguments.get("sector")
        )

    elif name == "get_sector_overview":
        return get_sector_overview(
            sector=arguments["sector"]
        )

    else:
        raise ValueError(f"Unknown tool: {name}")


# Attach dispatcher
server.call_tool = call_tool


if __name__ == "__main__":
    stdio_server(server)
