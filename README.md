# Cartloop Exercise

## Technologies
```
  Django 3.2.7
  Python 3.9.7
  Postman - testing purpose
```

## Project setup
```
django-admin startproject storefront
```

## Application setup
```
django-admin startapp cartloop_exercise
```

## Virtual environment setup
```
pip install pipenv
pipenv install django
```

## Rest Framework setup
```
pip install djangorestframework
pip install markdown
pip install django-filter
```

### Models Migration
```
python manage.py makemigration
python manage.py migrate
```

### Models Migration
```
python manage.py makemigration
python manage.py migrate
```

### Implementation
```
7 Models according to given data structure - most of them are mapped with ForeignKeys
2 ModelSerializer - used in creating both POST requests view methods: create_conversation and create_chat
4 endpoints:(base url: http://localhost:8000/)
  - POST: cartloop/conversations/ - create a new conversation
  - GET:  cartloop/conversations/<int:id>/ - return the details of a conversation following the given JSON structure
  - POST: cartloop/chats/ - create a new chat for the specified conversation
  - GET:  cartloop/chats/<int:id>/ - return the details of a chat following the given JSON structure
```

### Running and testing flow - with Postman

 POST: http://localhost:8000/cartloop/conversations/
```
  POST request in Postman with a JSON body like:
      {
        "store_id": 2,
        "client_id": 11,
        "operator_id": 2
      }
```

 GET:  http://localhost:8000/cartloop/conversations/<int:id>/
 ```
  GET request in Postman. It uses the given id from the url's body.
```

 POST: http://localhost:8000/cartloop/chats/
 ```
   POST request in Postman with a JSON body like:
      {
        "conversation_id": 2, 
        "payload": "Hello {{ client_first_name }}. This is {{ operator_full_name }}.\nHere is your discount code: {{ discount_code }}!",
        "discount_id": 2
      }
```

 GET:  http://localhost:8000/cartloop/chats/<int:id>/
 ```
  GET request in Postman. It uses the given id from the url's body.
```

!! All the other amount of data was manually added in DB through Django Admin. There's only a small piece of data, added only for testing purpose.
