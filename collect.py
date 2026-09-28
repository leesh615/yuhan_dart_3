from config import API_KEY,CORP_CODE,FS_DIV,YEARS,RAW_DIR
from dart_client import fetch_financials,save_raw
def main():
    for year in YEARS:
        print("수집:",year)
        save_raw(fetch_financials(API_KEY,CORP_CODE,year,FS_DIV),RAW_DIR/f"yuhan_{year}_{FS_DIV}.json")
if __name__=="__main__": main()
