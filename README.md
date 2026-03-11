# Tomorrow Weather Briefing Bot

매일 저녁 8시 15분에 내일 날씨와 공기질을 브리핑해 주는 텔레그램 봇 서비스입니다.

## 기존 프로젝트와 차이점
- 아침에 "어제 vs 오늘"을 비교하던 방식에서 벗어나, 저녁에 "오늘 vs 내일"을 미리 비교합니다.
- 복장/우산/마스크 챙기기 등 내일 외출 준비를 돕는 생활 밀착형 알림을 제공합니다.
- 기상청, AirKorea 등 한국 특화 공공 데이터를 활용합니다.

## 기능 특징
- **다지역 지원**: 한 번에 여러 지역의 날씨 정보를 조회하고 순차적으로 브리핑을 전송합니다.
- **안정성**: 한 지역의 조회가 실패하더라도 나머지 지역은 정상적으로 발송합니다. 공기질 API 장애 시 날씨 정보만 발송하는 Fallback 로직을 탑재했습니다.
- **행동 추천 알고리즘**: 오늘과 내일의 아침, 낮, 저녁 기온 차를 계산하여 옷차림을 조언합니다.

## 설치 및 실행 방법

### 1. 레포지토리 클론
```bash
git clone <repository-url>
cd tomorrow-weather-briefing-bot
```

### 2. 패키지 설치
Python 3.11 이상을 권장합니다.
```bash
pip install -r requirements.txt
```

### 3. 환경변수 설정
`.env.example` 파일을 복사하여 `.env` 파일을 생성하고 내용을 채웁니다.
```bash
cp .env.example .env
```

### 4. 텔레그램 봇 생성 및 Chat ID 확인
1. 텔레그램에서 `BotFather`를 검색하여 봇을 생성하고 HTTP API 토큰을 발급받아 `TELEGRAM_BOT_TOKEN`에 넣습니다.
2. 생성한 봇에 메시지를 보낸 후, `https://api.telegram.org/bot<TOKEN>/getUpdates` 를 브라우저나 curl로 열어 `chat_id`를 확인하고 `TELEGRAM_CHAT_ID`에 넣습니다.

### 5. API 키 준비
공공데이터포털(data.go.kr)에서 다음 두 가지 API 활용 신청을 한 후 서비스 키(디코딩)를 환경변수에 넣습니다.
- **기상청_단기예보 ((구)_동네예보) 조회서비스**: `KMA_SERVICE_KEY`
- **한국환경공단_에어코리아_대기오염정보**: `AIRKOREA_SERVICE_KEY`

### 6. 로컬 실행
```bash
python app.py
```

## GitHub Actions 자동 실행 설정

매일 저녁 자동 실행을 위해 `.github/workflows/evening_weather.yml`이 포함되어 있습니다.
GitHub 저장소의 `Settings` -> `Secrets and variables` -> `Actions`에 아래 내용들을 Secret으로 추가하세요.
- `KMA_SERVICE_KEY`
- `AIRKOREA_SERVICE_KEY`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `LOCATIONS_JSON` (또는 `LOCATIONS`)
- `TIMEZONE` (기본값: Asia/Seoul 사용 시 생략 가능)

> **Cron 설정**: 한국시간(KST) 저녁 8시 15분은 UTC 기준 오전 11시 15분이므로 `15 11 * * *` 로 설정되어 있습니다.

## 메시지 예시
📍 **서울특별시 강남구 역삼동**

📅 **오늘 (2026.03.11 (수))**
🌡️ 최고: 6.9°C / 최저: -4.3°C
💧 강수량: 0.0mm (확률: 0%)

📅 **내일 (2026.03.12 (목))**
🌡️ 최고: 7.6°C / 최저: -1.0°C
💧 강수량: 0.0mm (확률: 0%)
🔹 미세먼지: 미세(보통/43), 초미세(나쁨/30)

🗣️ **오늘 vs 내일 비교**
🔹 아침 기온: 오늘보다 3.3도 높아요.
🔹 낮 기온: 오늘보다 1.2도 높아요.
🔹 저녁 기온: 오늘보다 0.2도 낮아요.
🔹 낮에는 오늘보다 조금 더 가볍게 입어도 괜찮아요.
🔹 마스크를 챙기세요. (공기질 나쁨 이상)

## 트러블슈팅
1. **API Timeout (응답 없음)**: 공공 API 특성상 가끔 응답이 늦어질 수 있으며, 이에 대응해 최대 3회 재시도하도록 설정되어 있습니다. 계속 실패하면 로그에 "[실패]"가 기록됩니다.
2. **일부 지역만 실패**: JSON 지역 설정에서 `nx`, `ny` 또는 `station` 값이 올바른지 확인하세요. 한 지역이 실패해도 다른 지역 알림은 정상 발송됩니다.
3. **텔레그램 발송 실패**: 토큰이나 Chat ID가 유효한지 확인하고 봇 차단(block) 상태가 아닌지 점검하세요.
