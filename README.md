# Fastapi-Auth
Модуль аутентификации для Fastapi

## Установка
1. Необходимо склонировать модуль в любую папку своего проекта

```git clone https://github.com/PozyStark/fastapi_auth.git```

2. Перед установкой необходимо установить все необходимые зависимости из **requirements.txt**

```pip install -r requirements.txt```

3. Проиницализировать Alembic (eсли в проекте уже используется Alembic этот шаг можно пропустить)

```alembic init alembic```

4. Добавить **sqlalchemy.url** вашей базы данных в **alembic.ini** подробное описание **url** доступно на сайте [sqlachemy](https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls)

5. В **alembic/env.py** импортировать **metadata** из **models.py** и прописать её в **target_metadata** 

```from models import metadata```

```target_metadata = metadata```

6. Произвести миграцию моделей в базу данных

```alembic revision --autogenerate -m "add fastapi-auth models"```

```alembic upgrade head```

## Документация

Модуль может работать как самостоятельное приложение для аутентификации для этого можно просто запустить **main:app** используя **uvicorn**, **hypercorn** или **gunicorn**.
Средства запуска подробнее описаны на сайте официальной документации Fastapi [развертывание](https://fastapi.tiangolo.com/ru/deployment/)

### Запуск
```uvicorn main:app --reload```

так же есть возможность импортировать основные **роуты** в свое приложение

``` from routes import fastapi_auth_routes```

```app.include_router(fastapi_auth_routes)```

### Базовые роуты:

* **/registration** - предназначен для регистрации пользователя
* **/token** - авторизация пользователя (получаение токенов)
* **/token-verify** - проверка времени жизни токена
* **/token-refresh** - обновление пары токенов
* **/logout** - завершение жизни токена
* **/close-all-tokens** - завершение всех открытых пользователем токенов
* **/close-all-tokens-exclude-current** - завершение всех открытых пользователем токенов за исключением текущего

Так же с подробным описанием роутов и запросов можно ознакомиться в автоматичекой документации **Fastapi** при старте.

### Применение:

За проверку аутентификации отвечает класс **BearerAuth** чтобы указать что роут требует аутентификации достаточно указать данный класс в зависимости.

```
from dependencies import BearerAuth
from permissions import IsAuthenticated

@auth_routers.get("/protected-url")
async def protected_url(
    auth_request: Annotated[
        AuthRequest,
        Depends(
            BearerAuth(
                required_permissions=[IsAuthenticated]
            )
        )
    ]
):
    return {"detail": "you are authinticated"}
```