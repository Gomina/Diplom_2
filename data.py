
# класс TestUser (TU)
class TU:

    # правильный пользователь 1
    User_1 = {
            "email": 'ivan@gmail.com',
            "password": '123456',
            "name": 'Иван'
        }

    # некорректный пользователь 2, без имени
    User_2 = {
            "email": 'ivan@gmail.com',
            "password": '123456',
            "name": ''
        }

    # некорректный пользователь 3, без пароля
    User_3 = {
            "email": 'peter.1@gmail.com',
            "password": '',
            "name": 'Петр 1'
        }

    # некорректный пользователь 4, без почты
    User_4 = {
            "email": '',
            "password": '123456',
            "name": 'Петр 1'
        }

    # правильный пользователь 5
    User_5 = {
            "email": 'petr1@gmail.com',
            "password": '123456',
            "name": 'Петр 1'
        }

    # неверный пароль для пользователя 1
    User_6 = {
        "email": 'ivan@gmail.com',
        "password": '111111',
        "name": 'Иван'
    }


    # неверная почта для пользователя 1
    User_7 = {
            "email": 'egor@gmail.com',
            "password": '123456',
            "name": 'Иван'
        }

    # изменение данных для пользователя 1
    User_8 = {
            "email": 'ivan_ivanov@gmail.com',
            "password": '654321',
            "name": 'Иван Иванов'
        }

    # тело ответа при cоздании пользователя, если пользователь существует
    BODY_ANSWER_USER_EXISTS = "User already exists"

    # тело ответа при cоздании пользователя, без одного из обязательных полей
    BODY_ANSWER_ONE_FIELDS_NOT_FILLED_IN = "Email, password and name are required fields"

    # тело ответа при неуспешной авторизации
    BODY_ANSWER_AUTHORIZATION_FAILED = "email or password are incorrect"

    # тело ответа при изменении данных пользователя, если он авторизован, но не залогинин
    BODY_ANSWER_YOU_MUST_BE_LOGGED_IN = "You should be authorised"

    # тело ответа неуспешное изменение почты авторизованного пользователя, если такая почта уже есть у другого пользователя
    BODY_ANSWER_ANOTHER_USER_ALREADY_HAS_THIS_EMAIL = "User with such email already exists"




# класс TestOrder (TO)
class TO:
    # булка - Флюоресцентная булка
    ID_BUN_FLUORESCENT = "61c0c5a71d1f82001bdaaa6d"

    # ингредиент Говяжий метеорит
    ID_BEEF_METEORITE = "61c0c5a71d1f82001bdaaa70"

    # ингредиент соус Space Sauce
    ID_SPACE_SAUCE = "61c0c5a71d1f82001bdaaa73"

    # ингредиент c несуществующим ID
    ID_NON_EXISTENT_INGREDIENT = '111there1is1no1such1id'

    # тело ответа при создании заказа, если не передать ни один ингредиент
    BODY_ANSWER_NO_INGREDIENTS = "Ingredient ids must be provided"

    # тело ответа при запросе заказов конкретного пользователя, если выполнить запрос без авторизации
    BODY_ANSWER_REQUESTING_USER_ORDERS_WITHOUT_AUTHORIZATION = "You should be authorised"