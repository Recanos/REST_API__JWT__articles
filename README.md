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
curl --location 'http://localhost:8000/api/register/' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=ZSa81qNmrZiVZ3X0QyhFAdSn8GiVjoVtARdKx3ZgtJvxxHmWjqJxR1U7gMUOOCTR' \
--data '{
    "username" : "qwerty123",
    "password" : "1233343Ww"
}'
```
Пример postman:

(images/register.png)

После успешной регистрации пользователь может аутентифицироваться и получить JWT токены для доступа к защищенным маршрутам API

### Получение JWT токенов

Для получения JWT токенов, необходимо выполнить POST запрос на эндпоинт `/api/token/`, передав логин и пароль пользователя. В ответ на успешный запрос возвращаются access и refresh токены.

Пример запроса на получение токенов:

```bash
curl --location 'http://localhost:8000/api/token/' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=ZSa81qNmrZiVZ3X0QyhFAdSn8GiVjoVtARdKx3ZgtJvxxHmWjqJxR1U7gMUOOCTR' \
--data '{
    "username" : "qwerty123",
    "password" : "1233343Ww"
}'
```
Пример postman:

## Обновление Access токена

Когда срок жизни access токена истекает, можно получить новый с помощью refresh токена, отправив POST запрос на /api/token/refresh/

Пример запроса для обновления access токена:

```bash
curl --location 'http://localhost:8000/api/token/refresh/' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=ZSa81qNmrZiVZ3X0QyhFAdSn8GiVjoVtARdKx3ZgtJvxxHmWjqJxR1U7gMUOOCTR' \
--data '{
"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNDM5NTQwOSwiaWF0IjoxNzE0MzA5MDA5LCJqdGkiOiI2NGY5OTg0ZjMxZjg0NDhhOGJlY2RmZTE1NGU0MjYxZiIsInVzZXJfaWQiOjEzfQ.evvXfOXvINEv6guaGgMJWJWkbK20uT6g-S8tko45xoA"
}'
```
Пример postman:

##Проверка JWT токена

Для проверки валидности access токена можно использовать эндпоинт /api/token/verify/

Пример запроса на проверку токена:

```bash
curl --location 'http://localhost:8000/api/token/verify/' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=ZSa81qNmrZiVZ3X0QyhFAdSn8GiVjoVtARdKx3ZgtJvxxHmWjqJxR1U7gMUOOCTR' \
--data '{
"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE0MzA5Mzg3LCJpYXQiOjE3MTQzMDkwMDksImp0aSI6IjllYjQ4OGE3YmMyZDQ1MGE4MzdjOTYyYTExYWQwOTg1IiwidXNlcl9pZCI6MTN9.EvxxzXrZ2nyaxWk3vQLMZQOwIIHxIC63And9xnA5xew"
}'
```
Пример postman:

## Работа со статьями
API для статей позволяет выполнять API запросы для получения списка статей, создания новых статей, а также для редактирования и удаления существующих статей. Для доступа к этому функционалу используется эндпоинт /articles/.

### Получение списка всех статей

Чтобы получить список всех статей, отправьте GET запрос на /articles/

Пример запроса на получение списка статей:

```bash
curl --location 'http://localhost:8000/articles/' \
--header 'Cookie: csrftoken=ZSa81qNmrZiVZ3X0QyhFAdSn8GiVjoVtARdKx3ZgtJvxxHmWjqJxR1U7gMUOOCTR' \
--data ''
```
Пример postman:

### Создание новой статьи

Для создания новой статьи аутентифицированный пользователь должен отправить POST запрос с JSON содержащим заголовок и тело статьи на эндпоинт /articles/

Пример запроса для создания статьи:

```bash
curl --location 'http://localhost:8000/articles/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE0MzA5NzU4LCJpYXQiOjE3MTQzMDk0NTgsImp0aSI6IjBhMjAzZDczMWVjZjRlNDA5ZTNmYzRhMWQ2ZGExNmI4IiwidXNlcl9pZCI6MTN9.80Q-xVsoOl6xbmMieSjRPl8Paj83VVu9DGn1VPUxdlA' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=ZSa81qNmrZiVZ3X0QyhFAdSn8GiVjoVtARdKx3ZgtJvxxHmWjqJxR1U7gMUOOCTR' \
--data '{
    "header" : "Молоко",
    "body" : "Я покупаю молоко по пятницам и субботам"
}'
```

Пример postman:

### Обновление существующей статьи

Для обновления статьи отправьте PUT запрос с JSON содержащим новый заголовок и тело на /articles/{id}/, где {id} - это идентификатор статьи.

Пример запроса на обновление статьи:

```bash
curl --location --request PUT 'http://localhost:8000/articles/26/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE0MzA5NzU4LCJpYXQiOjE3MTQzMDk0NTgsImp0aSI6IjBhMjAzZDczMWVjZjRlNDA5ZTNmYzRhMWQ2ZGExNmI4IiwidXNlcl9pZCI6MTN9.80Q-xVsoOl6xbmMieSjRPl8Paj83VVu9DGn1VPUxdlA' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=ZSa81qNmrZiVZ3X0QyhFAdSn8GiVjoVtARdKx3ZgtJvxxHmWjqJxR1U7gMUOOCTR' \
--data '{
    "header" : "Квас",
    "body" : "Я покупаю квас по четвергам"
}'
```

Пример postman:

### Удаление статьи

Чтобы удалить статью, отправьте DELETE запрос на /articles/{id}/, где {id} - это идентификатор статьи.

Пример запроса для удаления статьи:

```bash
curl --location --request DELETE 'http://localhost:8000/articles/26/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE0MzA5NzU4LCJpYXQiOjE3MTQzMDk0NTgsImp0aSI6IjBhMjAzZDczMWVjZjRlNDA5ZTNmYzRhMWQ2ZGExNmI4IiwidXNlcl9pZCI6MTN9.80Q-xVsoOl6xbmMieSjRPl8Paj83VVu9DGn1VPUxdlA' \
--header 'Cookie: csrftoken=ZSa81qNmrZiVZ3X0QyhFAdSn8GiVjoVtARdKx3ZgtJvxxHmWjqJxR1U7gMUOOCTR' \
--data ''
```

Пример postman:

## Дополнительно

- Я оставил заполненную базу данных, чтобы можно было произвести какую-либо работу с данными, добавленными раньше 1го дня или другое (Для проверки редактирования статей в permissions.py можно поменять промежуток на минуты).
- При использовании access токена в поле Authorization нужно использовать слово Bearer (можно поменять в settings.py в разделе с simplejwt)
- В файле settings.py есть отдельный блок по работе с Django REST framework (работа с пагинацией, аутентификация через simplejwt)
- Так же в settings.py есть отдельный блок по работе с Simple JWT, вкючая алгоритм шифрования, время жизни токенов и тд
- 
