"""Run the SQL pipeline and export Tableau-ready CSVs to output/.

Usage:  python build.py
Needs:  pip install duckdb
Input:  data/raw/CCS_Permits.csv (download from opendata.minneapolismn.gov, "CCS Permits")
"""
from pathlib import Path
import duckdb

con = duckdb.connect("permits.duckdb")
for sql_file in sorted(Path("sql").glob("*.sql")):
    print(f"Running {sql_file.name}")
    con.execute(sql_file.read_text())

print("\nData quality check")
con.sql("SELECT * FROM dq_summary").show()
con.sql("SELECT * FROM dq_value_by_year").show()

Path("output").mkdir(exist_ok=True)
for table in ["dq_value_by_year", "yearly_by_type", "neighborhood_year",
              "commercial_contractors", "duration_by_work_type", "major_projects"]:
    con.execute(f"COPY {table} TO 'output/{table}.csv' (HEADER)")
    print(f"Wrote output/{table}.csv")
