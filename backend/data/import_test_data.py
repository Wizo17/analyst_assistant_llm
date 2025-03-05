import pandas as pd
from sqlalchemy import create_engine



def process_tale(table_name, schema="public", load_mode="replace"):
    # Connection to postgres
    engine = create_engine("postgresql://postgres:wilzo@localhost:5432/base_analyst_llm")

    # Import as DataFrame
    df = pd.read_csv(f"tests/{table_name}.txt")

    # Write in table
    df.to_sql(table_name, engine, if_exists=load_mode, index=False, schema=schema)


print("Import agency to postgres")
process_tale("agency")

print("Import booking_rules to postgres")
process_tale("booking_rules")

print("Import calendar_dates to postgres")
process_tale("calendar_dates")

print("Import calendar to postgres")
process_tale("calendar")

print("Import pathways to postgres")
process_tale("pathways")

print("Import routes to postgres")
process_tale("routes")

print("Import stop_extensions to postgres")
process_tale("stop_extensions")

print("Import stop_times to postgres")
process_tale("stop_times")

print("Import stops to postgres")
process_tale("stops")

print("Import ticketing_deep_links to postgres")
process_tale("ticketing_deep_links")

print("Import transfers to postgres")
process_tale("transfers")

print("Import trips to postgres")
process_tale("trips")


# pg_dump --username=postgres --password --schema-only base_analyst_llm > base_analyst_llm_export.sql
