import numpy as np,pandas as pd
from config import PROCESSED_DIR
def nm(x): return str(x).replace(" ","").replace("ㆍ","").replace("·","")
def acct(df,names,sj):
    x=df[df.sj_div.eq(sj)].copy(); x["_n"]=x.account_nm.map(nm)
    for n in names:
        n=nm(n); h=x[x._n.eq(n)]
        if not h.empty: return h.iloc[0].thstrm_amount_num
    for n in names:
        n=nm(n); h=x[x._n.str.contains(n,na=False)]
        if not h.empty: return h.iloc[0].thstrm_amount_num
    return np.nan
def av(df,y):
    x=df[df.bsns_year_requested.eq(y)]
    return {
      "매출액":acct(x,["매출액","수익(매출액)"],"IS"),
      "매출총이익":acct(x,["매출총이익"],"IS"),
      "영업이익":acct(x,["영업이익","영업이익(손실)"],"IS"),
      "당기순이익":acct(x,["당기순이익","당기순이익(손실)"],"CIS"),
      "총자산":acct(x,["자산총계"],"BS"),"유동자산":acct(x,["유동자산"],"BS"),
      "현금및현금성자산":acct(x,["현금및현금성자산"],"BS"),
      "매출채권":acct(x,["매출채권","매출채권및기타채권"],"BS"),
      "재고자산":acct(x,["재고자산"],"BS"),"총부채":acct(x,["부채총계"],"BS"),
      "유동부채":acct(x,["유동부채"],"BS"),"매입채무":acct(x,["매입채무","매입채무및기타채무"],"BS"),
      "자본총계":acct(x,["자본총계"],"BS"),
      "영업활동현금흐름":acct(x,["영업활동현금흐름"],"CF"),
      "투자활동현금흐름":acct(x,["투자활동현금흐름"],"CF"),
      "재무활동현금흐름":acct(x,["재무활동현금흐름"],"CF"),
      "이자비용":acct(x,["이자비용","금융비용"],"IS")
    }
def div(a,b): return np.nan if pd.isna(a) or pd.isna(b) or b==0 else a/b
def avg(a,b): return np.nan if pd.isna(a) or pd.isna(b) else (a+b)/2
def main():
    df=pd.read_csv(PROCESSED_DIR/"dart_financials_normalized.csv"); years=sorted(df.bsns_year_requested.unique()); vals={y:av(df,y) for y in years}; out=[]
    for i,y in enumerate(years):
        v=vals[y]; p=vals[years[i-1]] if i else None
        aa=avg(v["총자산"],p["총자산"]) if p else np.nan; ae=avg(v["자본총계"],p["자본총계"]) if p else np.nan
        ar=avg(v["매출채권"],p["매출채권"]) if p else np.nan; inv=avg(v["재고자산"],p["재고자산"]) if p else np.nan; ap=avg(v["매입채무"],p["매입채무"]) if p else np.nan
        cogs=v["매출액"]-v["매출총이익"] if pd.notna(v["매출액"]) and pd.notna(v["매출총이익"]) else np.nan
        r=dict(v); r["연도"]=y
        r.update({
          "매출증가율":div(v["매출액"],p["매출액"])-1 if p and pd.notna(v["매출액"]) and pd.notna(p["매출액"]) else np.nan,
          "매출총이익률":div(v["매출총이익"],v["매출액"]),"영업이익률":div(v["영업이익"],v["매출액"]),"순이익률":div(v["당기순이익"],v["매출액"]),
          "ROA":div(v["당기순이익"],aa),"ROE":div(v["당기순이익"],ae),
          "유동비율":div(v["유동자산"],v["유동부채"]),"당좌비율":div(v["유동자산"]-v["재고자산"],v["유동부채"]),
          "부채비율":div(v["총부채"],v["자본총계"]),"자기자본비율":div(v["자본총계"],v["총자산"]),
          "이자보상배율":div(v["영업이익"],v["이자비용"]),"총자산회전율":div(v["매출액"],aa),
          "DSO":div(ar*365,v["매출액"]),"DIO":div(inv*365,cogs),"DPO":div(ap*365,cogs),
          "CFO/순이익":div(v["영업활동현금흐름"],v["당기순이익"]),
          "FCF":np.nan,"순차입금":np.nan,"순차입금/EBITDA":np.nan
        })
        r["CCC"]=r["DSO"]+r["DIO"]-r["DPO"] if all(pd.notna(r[k]) for k in ["DSO","DIO","DPO"]) else np.nan
        out.append(r)
    pd.DataFrame(out).to_csv(PROCESSED_DIR/"financial_ratios.csv",index=False,encoding="utf-8-sig")
if __name__=="__main__": main()
