import json,pandas as pd
from config import RAW_DIR,PROCESSED_DIR,YEARS,FS_DIV
def num(x):
    try: return float(str(x).replace(",",""))
    except: return None
def main():
    rows=[]
    for year in YEARS:
        p=RAW_DIR/f"yuhan_{year}_{FS_DIV}.json"
        if not p.exists(): continue
        for r in json.loads(p.read_text(encoding="utf-8")).get("list",[]):
            q=dict(r); q["bsns_year_requested"]=year
            for k in ["thstrm_amount","frmtrm_amount","bfefrmtrm_amount"]:
                q[k+"_num"]=num(q.get(k))
            rows.append(q)
    df=pd.DataFrame(rows)
    if df.empty: raise SystemExit("원천 데이터가 없습니다.")
    df.to_csv(PROCESSED_DIR/"dart_financials_raw.csv",index=False,encoding="utf-8-sig")
    cols=["bsns_year_requested","sj_div","account_nm","account_id","thstrm_amount_num","frmtrm_amount_num","bfefrmtrm_amount_num","currency"]
    df[[c for c in cols if c in df]].to_csv(PROCESSED_DIR/"dart_financials_normalized.csv",index=False,encoding="utf-8-sig")
if __name__=="__main__": main()
