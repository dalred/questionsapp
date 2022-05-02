http://skypro-dal.ga/
##### Список допустимых эндпойнтов
> flask routes

| Endpoint     | Methods      | Rule  |
| :---: |   :---:       | :---: |
```doc                         GET                 /
questions_question_view     DELETE, GET, PATCH  /questions/<int:id>/
questions_questions_view    POST                /questions/ask/
questions_questions_view_2  GET, POST           /questions/
restx_doc.static            GET                 /swaggerui/<path:filename>
root                        GET                 /
specs                       GET                 /swagger.json
static                      GET                 /static/<path:filename>
```
###### Пример POST запроса на  
http://skypro-dal.ga/questions/ask/
```
{
"questions_num": 2
}
```
###### Пример ответа сервера
```json
{
    "question": "This former Berlin Wall checkpoint, where you can see instruments of escape used by East Germans",
    "answer": "Checkpoint Charlie",
    "created_at": "2015-01-22T02:28:51.157000",
    "id_": 3
}
```

##### MVC
![MVC](https://user-images.githubusercontent.com/25077706/160255834-4f21ae0b-22c3-4a48-9bd9-320f462446a9.png)
