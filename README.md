# 유한양행 DART 재무분석

OpenDART의 단일회사 전체 재무제표 API를 이용해 유한양행의 연결재무제표를 수집하고 주요 재무데이터와 재무비율을 계산하는 프로젝트입니다.

- 기준: 연결재무제표(CFS)
- 보고서: 사업보고서(11011)
- 기간: 2020~2025 (2020은 평균잔액/증가율 계산용)
- 원천: 금융감독원 OpenDART
- 분석 기준: 첨부된 「재무제표 및 재무비율 실무 가이드」
- 대시보드: GitHub Pages 정적 HTML
- 자동화: GitHub Actions

## 실행
```bash
pip install -r requirements.txt
# DART_API_KEY, DART_CORP_CODE 설정
cd src
python pipeline.py
cd ..
python dashboard/generate.py
```
