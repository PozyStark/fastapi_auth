# Fastapi-Auth
Долгие поиски решения для полноценной аутентификации по паре токенов чтобы можно было контролировать актуальность токена привели к написанию этого модуля.

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
____
### Запуск
```uvicorn main:app --reload```

так же есть возможность импортировать основные **роуты** в свое приложение

``` from routes import fastapi_auth_routes```

```app.include_router(fastapi_auth_routes)```
____
### Базовые роуты:
* **/registration** - предназначен для регистрации пользователя
* **/token** - авторизация пользователя (получаение токенов)
* **/token-verify** - проверка времени жизни токена
* **/token-refresh** - обновление пары токенов
* **/logout** - завершение жизни токена
* **/close-all-tokens** - завершение всех открытых пользователем токенов
* **/close-all-tokens-exclude-current** - завершение всех открытых пользователем токенов за исключением текущего

Так же с подробным описанием роутов и запросов можно ознакомиться в автоматичекой документации **Fastapi** при старте.
____
### Применение
За проверку аутентификации отвечает класс **BearerAuth** чтобы указать что роут требует аутентификации достаточно указать данный класс в зависимости.

Пример:
```python
from dependencies import BearerAuth, AuthRequest

@auth_routers.get("/protected-url")
async def protected_url(
    auth_request: Annotated[AuthRequest, Depends(BearerAuth())]
):
    return {"detail": "you are authinticated"}
```

На данном примере роут доступен всем пользователям и после получения информации с токена будет возвращен AuthRequest с информацией о пользователе.
Так же это можно указать в явном виде.

Пример:
```python
from dependencies import BearerAuth, AuthRequest
from permissions import AllowAny

@auth_routers.get("/protected-url")
async def protected_url(
    auth_request: Annotated[
        AuthRequest, Depends(BearerAuth(required_permissions=[AllowAny]))
    ]
):
    return {"detail": "you are authinticated"}
```
____
### Режим поиска токена
Существует два режима поиска токена **BearerAuth.COOKIE_MODE** и **BearerAuth.HEADER_MODE**.
Для этого в конструкторе определен параметр **search_mode**.
Этот параметр возможно задать в конфигурации (будет применен для всех роутов по умолчанию) или задать его в индивидуальном порядке

```python
config.py

# Настройки режима поиска токена
SEARCH_MODE = SearchMode.COOKIE_MODE
```

Пример:
```python
from dependencies import BearerAuth, AuthRequest
from permissions import AllowAny

@auth_routers.get("/protected-url")
async def protected_url(
    auth_request: Annotated[
        AuthRequest, Depends(BearerAuth(search_mode=BearerAuth.COOKIE_MODE))
    ]
):
    return {"detail": "you are authinticated"}
```
____
### Ограничение доступа
Для ограничения доступа в классе **BearerAuth** определен список **required_permissions** в него необходимо добавить те доступы которые должны быть у пользователя. На примере ниже указан роут доступ к которому могут получить только те пользователи которые относятся к **SuperUser**

Пример:
```python
from dependencies import BearerAuth, AuthRequest
from permissions import IsSuperUser

@auth_routers.get("/protected-url")
async def protected_url(
    auth_request: Annotated[
        AuthRequest, Depends(BearerAuth(required_permissions=[IsSuperUser]))
    ]
):
    return {"detail": "you are authinticated"}
```
____
### Стандартные доступы
В модуле **permissions.py** определены несколько стандартных доступов

* **AllowAny** - доступ к роуту предоставляется всем пользователям
* **IsAuthenticated** - доступ предоставляется только авторизованным пользователям
* **IsSuperUser** - доступ предоставляется пользователям с правами супер пользователя
* **IsAdminUser** - доступ предоставляется пользователям с правами администратора
* **IsStuff** - доступ предоставляется пользователям с правами работы с админ панелью
____
### Пользовательские доступы
Для того чтобы указать не стандартный доступ в модуле **permissions.py** определены классы
* **StrPermission** - для того чтобы указать необходимый пользовательский доступ
* **StrRole** - для того чтобы указать необходимую роль
* **StrGroup** - для того чтобы указать необходимую группу

В примере доступ к роуту будет предоставлен только тем пользователям которые относятся к группе **site_creators**
классы **StrPermission** и **StrRole** работают по аналогии

Пример:
```python
from dependencies import BearerAuth, AuthRequest
from permissions import StrGroup

@auth_routers.get("/protected-url")
async def protected_url(
    auth_request: Annotated[
        AuthRequest, Depends(BearerAuth(required_permissions=[StrGroup('site_creators')]))
    ]
):
    return {"detail": "you are authinticated"}
```
____
### Собственные классы доступов
Есть возможность определить свой собственный класс унаследовавшись от **BasePermission**

Пример:
```python
from dependencies import BearerAuth, AuthRequest
from permissions import BasePermission

class IsSiteCreator(BasePermission):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def has_permission(self) -> HTTPException:
        super().has_permission()
        if not 'site_creator' in self.auth_request.user.user_groups:
            self.exception(f'Not allowed has no group site_creator')

@auth_routers.get("/protected-url")
async def protected_url(
    auth_request: Annotated[
        AuthRequest, Depends(BearerAuth(required_permissions=[IsSiteCreator]))
    ]
):
    return {"detail": "you are authinticated"}
```
____
### Объект AuthRequest
После проверки доступов и валидации данных **BearerAuth** возвращает объект **AuthRequest**. Он содержит в себе информацию о пользователе, его доступах и аутентификации

* **request:Request** - базовый объект запроса
* **request_token:RequestToken** - схема с информацией содержащейся в токене
* **user:RequestUser** - схема с информацией о пользователе

```python
class RequestToken(BaseModel):
    token: str | None = None
    token_id: str | None = None
    temp_id: str | None = None
    user_id: str | None = None
```

```python
# Любой не авторизованный пользователь считается как анонимный

class RequestUser(BaseModel):
    id: str = None
    username: str = 'anonimus'
    email: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    is_authinticated: bool = False
    is_superuser: bool = False
    is_stuff: bool = False
    is_active: bool = False
    age: int | None = None
    avatar: str | None = None
    user_permissions: list | None = None
    user_roles: list | None = None
    user_groups: list | None = None
    created_at: datetime | None
    last_login: datetime | None
    last_updated: datetime | None
```

Пример:
```python
from dependencies import BearerAuth, AuthRequest
from permissions import BasePermission


@auth_routers.get("/protected-url")
async def protected_url(
    auth_request: Annotated[AuthRequest, Depends(BearerAuth())]
):
    name = auth_request.user.username
    token_id = auth_request.request_token.token_id
    return {"detail": f"Hello {name} your token is {token_id}"}
```
