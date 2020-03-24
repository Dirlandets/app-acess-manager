## Задача
Реализовать API, позволяющее:
- добавлять Create, 
- изменять Update, 
- просматривать Retrieve,
- удалять Delete

данные в модели "Приложения".

"Приложения" – это модель, которая хранит в себе внешние источники, которые будут обращаться к API. 

### Обязательные поля модели: 
- ID;
- Название приложения;
- Ключ API. 

Поле "Ключ API" нельзя менять через API напрямую, должен быть метод, позволяющий создать новый ключ API.

После добавления приложения – должна быть возможность использовать "Ключ API" созданного приложения для осуществления запросов к методу /api/test, метод должен возвращать JSON, содержащий всю информацию о приложении.

### Использовать следующие технологии: 
- Django 2.2.7,
- Django REST framework.


## Результат выполнения задачи:
### Инструкция по разворачиванию приложения (в docker или локально)
#### Поднять локально на 127.0.0.1:8000 
docker-compose -f docker-compose-dev.yml up --build

#### Мигрируем:
docker-compose -f docker-compose-dev.yml exec backend python manage.py makemigrations

docker-compose -f docker-compose-dev.yml exec backend python manage.py migrate

#### Грузим подготовленных пользователей и приложения
docker-compose -f docker-compose-dev.yml exec backend python manage.py loaddata db.json

##### Запустить тесты:
docker-compose -f docker-compose-dev.yml exec backend python manage.py test


### Авторизация: 
Пользователи:
myuser
developer (суперюзер)
Пароль: 1616dldl

Админка: 127.0.0.1:8000/secret-admin/

Интерфейс API: 127.0.0.1:8000/api/

### Получить список приложений которые принадлежат авторизованному пользователю.
- GET 127.0.0.1:8000/api/

### Добавить новое приложение
- POST 127.0.0.1:8000/api/ {'name': 'NewApp'}

### Тестировать приложение
127.0.0.1:8000/api/test/
В хедере запроса должен быть "Token": "{тестируемый токен}"
Если токен будет будет правильный, API вернет его данные.
Есди токен будет неправильный, API вернет 403.

### Получить инфу по приложению
GET 127.0.0.1:8000/api/{pk}/

### Изменить инфу по приложению
Доступно Имя и Пользователь если пользователь суперюзер если пользователь обычный он может только переименовывать свои приложения
- PUT 127.0.0.1:8000/api/{pk}/
- DELETE 127.0.0.1:8000/api/{pk}/
- PATCH 127.0.0.1:8000/api/{pk}/

#### Обновить токен
- GET 127.0.0.1:8000/api/{pk}/refresh/ -> вернет на GET 127.0.0.1:8000/api/{pk} но уже с обновленным токеном.


#### Особенности
Обычный пользователь может иметь много приложений но изменять и видеть он будет только свои.

Админ видит все.
