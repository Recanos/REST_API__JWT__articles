# REST_API__JWT__articles
Приложение, реализующее API с токенами авторизации (JWT), регистрацию и авторизацию пользователей, создание и работу с заметками

## Установка

```bash
git clone https://github.com/Recanos/REST_API__JWT__articles.git
cd REST_API__JWT__articles
python -m venv venv # Для линукса python3 -m venv venv
source venv/bin/activate # Для Windows используйте venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
```
Запустим север

```bash
python manage.py runserver
```

## JWT Authentication

https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html

Проект использует механизм аутентификации JSON Web Tokens (JWT) для безопасного контроля доступа к API. По умолчанию, JWT состоит из двух ключевых частей: access токена и refresh токена. Access токен используется для аутентификации и авторизации на API по различным маршрутам и имеет короткий срок жизни. Refresh токен используется для получения нового access токена без необходимости повторного ввода учетных данных и имеет более длительный срок жизни. 

### Регистрация пользователя

Для регистрации нового пользователя предусмотрен эндпоинт `/api/register/`. Для создания пользователя необходимо отправить POST запрос на этот адрес с JSON содержащим имя пользователя и пароль.

Пример запроса для регистрации пользователя:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "newuser", "password": "newpassword"}' http://localhost:8000/api/register/
```

После успешной регистрации пользователь может аутентифицироваться и получить JWT токены для доступа к защищенным маршрутам API

### Получение JWT токенов

Для получения JWT токенов, необходимо выполнить POST запрос на эндпоинт `/api/token/`, передав логин и пароль пользователя. В ответ на успешный запрос возвращаются access и refresh токены.

Пример запроса на получение токенов:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "yourusername", "password": "yourpassword"}' http://localhost:8000/api/token/
```

## Обновление Access токена

Когда срок жизни access токена истекает, можно получить новый с помощью refresh токена, отправив POST запрос на /api/token/refresh/

Пример запроса для обновления access токена:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"refresh": "yourrefreshtoken"}' http://localhost:8000/api/token/refresh/
```

##Проверка JWT токена

Для проверки валидности access токена можно использовать эндпоинт /api/token/verify/

Пример запроса на проверку токена:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"token": "youraccesstoken"}' http://localhost:8000/api/token/verify/
```
## Работа со статьями
API для статей позволяет выполнять API запросы для получения списка статей, создания новых статей, а также для редактирования и удаления существующих статей. Для доступа к этому функционалу используется эндпоинт /articles/.

### Получение списка всех статей

Чтобы получить список всех статей, отправьте GET запрос на /articles/

Пример запроса на получение списка статей:

```bash
curl -X GET http://localhost:8000/articles/
```

### Создание новой статьи

Для создания новой статьи аутентифицированный пользователь должен отправить POST запрос с JSON содержащим заголовок и тело статьи на эндпоинт /articles/

Пример запроса для создания статьи:

```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer youraccesstoken" -d '{"header": "Article Title", "body": "Content of the article."}' http://localhost:8000/articles/
```
### Обновление существующей статьи

Для обновления статьи отправьте PUT запрос с JSON содержащим новый заголовок и тело на /articles/{id}/, где {id} - это идентификатор статьи.

Пример запроса на обновление статьи:

```bash
curl -X PUT -H "Content-Type: application/json" -H "Authorization: Bearer youraccesstoken" -d '{"header": "Updated Title", "body": "Updated content."}' http://localhost:8000/articles/{id}/
```

### Удаление статьи

Чтобы удалить статью, отправьте DELETE запрос на /articles/{id}/, где {id} - это идентификатор статьи.

Пример запроса для удаления статьи:

```bash
curl -X DELETE -H "Authorization: Bearer youraccesstoken" http://localhost:8000/articles/{id}/
```

## Дополнительно

- Я оставил заполненную базу данных, чтобы можно было произвести какую-либо работу с данными, добавленными раньше 1го дня или другое (Для проверки редактирования статей в permissions.py можно поменять промежуток на минуты).
- При использовании access токена в поле Authorization нужно использовать слово Bearer (можно поменять в settings.py в разделе с simplejwt)
- В файле settings.py есть отдельный блок по работе с Django REST framework (работа с пагинацией, аутентификация через simplejwt)
- Так же в settings.py есть отдельный блок по работе с Simple JWT, вкючая алгоритм шифрования, время жизни токенов и тд
- 
