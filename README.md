🧠 MCP Financial Server

A Model Context Protocol (MCP) compliant server that exposes financial data tools over a Supabase PostgreSQL database.
The server supports stdio transport and provides structured tool-based access to company, financial, stock, analyst, and sector data.

🚀 Features

MCP-compliant Python server

Supabase PostgreSQL backend

Secure environment variable configuration

Modular tool-based architecture

Realistic financial dummy data

Supports stdio transport (Claude Desktop / Cursor compatible)

🛠️ Tech Stack

Python 3.10+

MCP Python SDK

Supabase (PostgreSQL)

dotenv

Faker (for seeding data)

📦 Project Structure
mcp-financial-server/
├── README.md
├── requirements.txt
├── .env.example
├── src/
│   ├── index.py
│   ├── config/
│   │   └── env.py
│   ├── db/
│   │   └── client.py
│   ├── tools/
│   │   ├── company_tools.py
│   │   ├── financial_tools.py
│   │   ├── stock_tools.py
│   │   ├── analyst_tools.py
│   │   └── sector_tools.py
│   └── utils/
│       └── errors.py
└── database/
    ├── schema.sql
    └── seed.sql

🔐 Environment Variables

Create a .env file using the template below:

SUPABASE_URL=https://<your-project-id>.supabase.co
SUPABASE_SERVICE_ROLE_KEY=<your-service-role-key>

🗄️ Database Setup

Create a Supabase project

Run database/schema.sql to create tables

Run database/seed.sql (or seed script) to insert dummy data

▶️ Running the Server

Activate virtual environment and run:

python -m src.index


The server will start using stdio transport.

🔧 Available MCP Tools
1. get_company_profile

Fetch company profile by ticker or name.

{
  "tool": "get_company_profile",
  "arguments": { "identifier": "AAPL" }
}

2. search_companies

Search companies using filters.

{
  "tool": "search_companies",
  "arguments": {
    "sector": "Technology",
    "country": "US"
  }
}

3. get_financial_report
{
  "tool": "get_financial_report",
  "arguments": {
    "ticker": "AAPL",
    "fiscal_year": 2023,
    "fiscal_quarter": "Q4"
  }
}

4. compare_companies
{
  "tool": "compare_companies",
  "arguments": {
    "tickers": ["AAPL", "MSFT"],
    "metrics": ["revenue", "net_income"]
  }
}

5. get_stock_price_history
{
  "tool": "get_stock_price_history",
  "arguments": {
    "ticker": "AAPL",
    "limit": 10
  }
}

6. get_analyst_ratings
{
  "tool": "get_analyst_ratings",
  "arguments": {
    "ticker": "AAPL"
  }
}

7. screen_stocks
{
  "tool": "screen_stocks",
  "arguments": {
    "min_revenue": 50000,
    "sector": "Technology"
  }
}

8. get_sector_overview
{
  "tool": "get_sector_overview",
  "arguments": {
    "sector": "Technology"
  }
}# mcp-financial-server
