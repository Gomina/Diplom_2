
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