# 초기 설정

1. OpenDART 인증키를 발급합니다: https://opendart.fss.or.kr/
2. DART 고유번호 조회에서 유한양행의 **8자리 corp_code**를 확인합니다. 종목코드 `000100`과 corp_code는 다릅니다.
3. GitHub 저장소 Settings → Secrets and variables → Actions에 다음을 등록합니다.
   - `DART_API_KEY`
   - `DART_CORP_CODE`
4. Settings → Pages → Source를 GitHub Actions로 설정합니다.
5. Actions → `Update Yuhan DART Financials`를 수동 실행합니다.

API 키는 코드나 파일에 직접 저장하지 않습니다.
