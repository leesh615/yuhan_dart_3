from pathlib import Path
import pandas as pd, json
BASE=Path(__file__).resolve().parents[1]
DATA=BASE/"data/processed/financial_ratios.csv"; OUT=BASE/"dashboard/index.html"
def fmt(v,p=False):
    if pd.isna(v): return "-"
    return f"{v*100:.2f}%" if p else f"{v:,.2f}"
def main():
    df=pd.read_csv(DATA).sort_values("연도"); z=df.iloc[-1]
    cards=[("매출액",fmt(z["매출액"])),("영업이익",fmt(z["영업이익"])),("당기순이익",fmt(z["당기순이익"])),("영업이익률",fmt(z["영업이익률"],1)),("ROE",fmt(z["ROE"],1)),("유동비율",fmt(z["유동비율"])),("부채비율",fmt(z["부채비율"],1)),("CFO/순이익",fmt(z["CFO/순이익"]))]
    cards_html="".join('<div class="card"><div class="label">'+k+'</div><div class="value">'+v+'</div></div>' for k,v in cards)
    rows=[]
    for _,r in df.iterrows():
        rows.append("<tr>"+"".join([
            f"<td>{int(r['연도'])}</td>",f"<td>{fmt(r['매출액'])}</td>",f"<td>{fmt(r['영업이익'])}</td>",
            f"<td>{fmt(r['당기순이익'])}</td>",f"<td>{fmt(r['영업이익률'],1)}</td>",f"<td>{fmt(r['ROA'],1)}</td>",
            f"<td>{fmt(r['ROE'],1)}</td>",f"<td>{fmt(r['유동비율'])}</td>",f"<td>{fmt(r['부채비율'],1)}</td>",f"<td>{fmt(r['CFO/순이익'])}</td>"
        ])+"</tr>")
    tpl=Path(__file__).with_name("template.html").read_text(encoding="utf-8")
    repl={
      "__CARDS__":cards_html,"__ROWS__":"".join(rows),
      "__YEARS__":json.dumps([int(x) for x in df["연도"]]),
      "__REVENUE__":json.dumps([None if pd.isna(x) else float(x) for x in df["매출액"]]),
      "__OPM__":json.dumps([None if pd.isna(x) else float(x*100) for x in df["영업이익률"]]),
      "__ROE__":json.dumps([None if pd.isna(x) else float(x*100) for x in df["ROE"]])
    }
    for a,b in repl.items(): tpl=tpl.replace(a,b)
    OUT.write_text(tpl,encoding="utf-8")
if __name__=="__main__": main()
