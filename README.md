# 기술과제: Server Developer (Internal Product)

본 문서는 기술 과제에서 요구하는 산출물의 명세를 설명합니다. 다음의 요구 사항을 만족하는 Django 서버 어플리케이션을 구현해 주세요.

# 개요

토스에서는 업무 메신저로 인큐베이터라는 솔루션을 사용하고 있습니다. 그리고 다양한 채널에서 다양한 팀원들이 업무에 대한 커뮤니케이션을 하며 메시지들이 만들어지고 이 메시지들을 수집 및 가공하여 사용하고 있습니다.

인큐베이터를 사용해 메신저에서 발생한 message, channel, user, channel-to-users (채널에 참여한 유저) 데이터를 조회할 수 있습니다. 인터널팀은 인큐베이터에서 제공하는 API를 기반으로 많은 데이터를 통합해서 보여주는 MessageList API를 만들었습니다.

인터널팀에서 해당 API를 제공한 이후 새로운 피드백을 받고 기능 개선을 하려고 합니다.

- MessageList API에서 불필요한 오버헤드가 발생하고 있어 속도가 매우 느려 DB 레이어를 사용한 통합 API 개선이 필요합니다.
- MessageList API가 특정 조건으로 조회되어야 하는 추가 기능이 필요합니다.
- 수많은 메시지 중 중요한 메시지를 놓칠 수 있어서 특정 메시지를 받은 팀원들에게 리마인드 메시지를 보낼 수 있는 기능이 추가로 필요합니다.

토스팀원 분들이 업무에 도움을 받을 수 있게

1. MessageList API를 개선해주세요
2. [인큐베이터 메시지 발송 API](#인큐베이터-메시지-발송-API)를 활용해서 MessageSend API를 구현해주세요

# 요구사항

1. MessageList API를 개선해주세요

- 메시지를 조회할 수 있는 기능
    - 채널 id list로 필터 돼서 조회할 수 있어야 합니다.```ex) ({url}?channel_id=ABC&channel_id=ABC2)```
    - 특정 유저의 닉네임으로 필터 돼서 조회할 수 있어야 합니다. ```ex) ({url}?nickname=ABC)```
    - 특정 메시지 내용으로 필터 돼서 조회할 수 있어야 합니다. ```ex) ({url}?message=신규가입)```
        - 메시지 목록에는 다음과 같은 정보가 포함되어야 합니다.
            - 메시지 ID
            - 메시지 내용
            - 메시지가 작성된 채널 정보
                - 메시지가 작성된 채널 ID
                - 메시지가 작성된 채널 이름
            - 메시지 작성자 유저정보
                - 메시지 작성자 유저 ID
                - 메시지 작성자 유저 닉네임
                - 메시지 작성자 유저가 참여되어있는 채널 ID 목록

2. MessageSend API를 완성해주세요

- 특정 메시지가 발송된 채널에 포함되어있는 유저들에게 메시지를 발송할 수 있는 기능
    - 메시지가 작성된 채널에 포함된 모든 유저에게 누락 없이 메시지가 발송 되어야 합니다.

추가 제약사항

- 모든 API는 500ms 이내에 응답을 주어야 합니다.

# 인큐베이터 어플리케이션 제공 데이터

## 인큐베이터 메시지 조회 API

### Endpoint

```
GET https://ipd-incubator.toss.im/api/v1/messages/
```

```
{
    "data": [
        {
            "id": "c6afeac5-5a7f-480c-8595-38e2cb4f2884",
            "message": "공무원의 신분과 정치적 중립성은 법률이 정하는 바에 의하여 보장된다.\n국군의 조직과 편성은 법률로 정한다. 신체장애자 및 질병·노령 기타의 사유로 생활능력이 없는 국민은 법률이 정하는 바에 의하여 국가의 보호를 받는다.\n외국인은 국제법과 조약이 정하는 바에 의하여 그 지위가 보장된다.",
            "channel_id": "CEYTL28JB373",
            "user_id": "U82VLI9QCR86",
            "created_at": "2021-02-03"
        },
        {
            "id": "f1cd0d11-0eae-4df8-9fb5-1a09f20e5b0f",
            "message": "대통령은 헌법과 법률이 정하는 바에 의하여 국군을 통수한다.\n대통령은 국민의 보통·평등·직접·비밀선거에 의하여 선출한다.",
            "channel_id": "C8L659GFQI2B",
            "user_id": "U7TWT612GY0T",
            "created_at": "2021-02-18"
        },
        .......
    ]
}
```

### Endpoint

```
GET https://ipd-incubator.toss.im/api/v1/messages/c6afeac5-5a7f-480c-8595-38e2cb4f2884/
```

```
{
    "data": {
        "id": "c6afeac5-5a7f-480c-8595-38e2cb4f2884",
        "message": "공무원의 신분과 정치적 중립성은 법률이 정하는 바에 의하여 보장된다.\n국군의 조직과 편성은 법률로 정한다. 신체장애자 및 질병·노령 기타의 사유로 생활능력이 없는 국민은 법률이 정하는 바에 의하여 국가의 보호를 받는다.\n외국인은 국제법과 조약이 정하는 바에 의하여 그 지위가 보장된다.",
        "channel_id": "CEYTL28JB373",
        "user_id": "U82VLI9QCR86",
        "created_at": "2021-02-03"
    }
}
```

## 인큐베이터 채널 조회 API

### Endpoint

```
GET https://ipd-incubator.toss.im/api/v1/channels/
```

```
{
    "data": [
        {
            "id": "CQ5VS6H6W1XN",
            "name": "studio"
        },
        {
            "id": "CQR2Z6XE60JV",
            "name": "disease"
        },
        ....
    ]
}
```

### Endpoint

```
GET https://ipd-incubator.toss.im/api/v1/channels/CQR2Z6XE60JV/
```

```
{
    "data": {
        "id": "CQR2Z6XE60JV",
        "name": "disease"
    }
}
```

## 인큐베이터 채널에 참여한 유저 조회 API

### Endpoint

```
GET https://ipd-incubator.toss.im/api/v1/channel-to-users/
```

```
{
    "data": [
        {
            "channel_id": "CQ5VS6H6W1XN",
            "user_id": "UN2A156IM0Z6"
        },
        {
            "channel_id": "CQ5VS6H6W1XN",
            "user_id": "UKAAHB7H1JRL"
        },
    ...
}
```

## 인큐베이터 유저 조회 API

### Endpoint

유저의 닉네임은 1시간마다 변경 될 수 있습니다.

```
GET https://ipd-incubator.toss.im/api/v1/users/
```

```
{
    "data": [
        {
            "id": "UCGLCDLSXTTI",
            "nickname": "수줍은 노루"
        },
        {
            "id": "U74SH6W99N25",
            "nickname": "탐스러운 노루"
        },
        {
            "id": "UFKWHPH7FWKR",
            "nickname": "둥그런 낙타"
        },
    ]
}
```

### Endpoint

```
GET https://ipd-incubator.toss.im/api/v1/users/UCGLCDLSXTTI/
```

```
{
    "data": {
        "id": "UCGLCDLSXTTI",
        "nickname": "약은 늪영양"
    }
}
```

## 인큐베이터 메시지 발송 API

### Endpoint

```
POST 'https://ipd-incubator.toss.im/api/v1/messages/'

{
    "user_id": "UFKWHPH7FWKR",
    "text": "리마인드 메시지입니다"
}
```

메시지 발송 API는 종종 실패할 수 있습니다

SUCCESS

```
{
    "success": true
}
```

FAIL

``` status code : 429
{
    "error": "잠시 후 다시 시도해주세요."
}
```

# 개발환경

바로 구현을 시작하실 수 있도록, 개발 환경을 미리 준비해두었습니다.

다음 명령을 사용하여 Django 서버를 시작할 수 있습니다.

```
pip install -r requirements.txt
python manage.py runserver runserver 0.0.0.0:28172
```

or

```
docker-compose up --build
```

# 검토환경

과제물을 보다 정확하게 검토하기 위해, 저희는 docker-compose up --build 명령을 실행하여 제출하신 과제물을 실행합니다. 제출 전, 해당 명령을 실행하여 과제물이 정상적으로 작동하는지 꼭 확인해주세요

# FAQ

- Django REST Framework를 사용해도 되나요?
    - 네, Django와 함께 사용할 수 있는 어떤 라이브러리도 사용하셔도 괜찮습니다.
    - 검토 환경에서 해당 라이브러리가 잘 설치되도록 주의해주세요.

- Flask/FastAPI를 사용해도 되나요?
    - 아니오, 웹 프레임워크는 Django를 사용해주세요

- SQLite 대신 MySQL/PostgreSQL을 사용해도 되나요?
    - 네, 사용하셔도 됩니다.
    - 단, docker-compose.yml 등에 해당 DB를 구동할 수 있는 설정을 추가해주세요.

- 제공된 파일을 수정해도 되나요?
    - 과제물이 정상적으로 작동하기 위해 실행되어야 하는 작업이 있거나 추가적으로 필요한 의존성이 있다면, docker-compose.yml , Dockerfile , requirements.txt 을 포함한 모든 파일을 수정하셔도 괜찮습니다. 가급적 docker-compose up 명령만으로 검토 환경을 구성할 수 있도록 개발해주시는 것을 권장드리지만, 그 외의 명령이 실행되어야 한다면 README 등에 명시해주시기 바랍니다.

# 저작권

해당 문제에 대한 저작권은 주식회사 비바리퍼블리카(이하 '회사')에게 있으며 수령자는 오로지 채용을 위한 목적으로만 해당 문제를 활용할 수 있습 니다. 사유를 불문하고 해당 문제의 전부 또는 일부를 공개, 게재, 배포, 제3자에게 제공 하는 등의 일체의 누설 행위에 대해서는 저작권법에 의한 민. 형사상의 책임을 질 수 있습니다. 아울러 이러한 누설 금지 행위에는 문제의 문구를 변형하여 그 취지를 알 수 있도록 하는 경우 포함됩니다.

