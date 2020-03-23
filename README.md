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

### Результат выполнения задачи:
- исходный код приложения в github
- инструкция по разворачиванию приложения (в docker или локально)
- инструкция по работе с запросами к API: 
  - как авторизоваться, 
  - как добавить, 
  - как удалить и т.д.