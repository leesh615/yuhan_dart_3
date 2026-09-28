import json,requests
BASE_URL="https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json"
def fetch_financials(api_key,corp_code,year,fs_div="CFS",report_code="11011"):
    if not api_key: raise ValueError("DART_API_KEY가 없습니다.")
    if not corp_code: raise ValueError("DART_CORP_CODE가 없습니다.")
    params={"crtfc_key":api_key,"corp_code":corp_code,"bsns_year":str(year),"reprt_code":report_code,"fs_div":fs_div}
    r=requests.get(BASE_URL,params=params,timeout=30); r.raise_for_status(); data=r.json()
    if data.get("status")!="000": raise RuntimeError(f"DART API 오류: {data.get('status')} / {data.get('message')}")
    return data
def save_raw(data,path):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
