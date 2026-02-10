from src.db.client import supabase
res = supabase.table("companies").select("ticker,name").limit(1).execute()
print(res.data)
