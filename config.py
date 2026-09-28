import os
from pathlib import Path
BASE_DIR=Path(__file__).resolve().parents[1]
RAW_DIR=BASE_DIR/"data/raw"; PROCESSED_DIR=BASE_DIR/"data/processed"; DASHBOARD_DIR=BASE_DIR/"dashboard"
API_KEY=os.getenv("DART_API_KEY",""); CORP_CODE=os.getenv("DART_CORP_CODE","")
FS_DIV=os.getenv("DART_FS_DIV","CFS")
YEARS=[int(x) for x in os.getenv("DART_YEARS","2020,2021,2022,2023,2024,2025").split(",") if x.strip()]
REPORT_CODE="11011"
for p in [RAW_DIR,PROCESSED_DIR,DASHBOARD_DIR]: p.mkdir(parents=True,exist_ok=True)
