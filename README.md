# Diplom_2
Сделаны тесты для  Stellar Burgers
URL сайта https://stellarburgers.nomoreparties.site/

Тесты для пользователя.
Создание пользователя:
test_creation_unique_user - тест на успешное создание уникального пользователя
test_re_creating_user - тест на ошибку при создании пользователя, который уже создан
test_creation_user_without_one_data - тест на ошибку при создании пользователя без одного из обязательных полей
Логин пользователя:
test_login_user_with_data - тест успешной авторизации пользователя с заданными параметрами
test_login_user_unfaithful_password - тест неуспешной авторизации пользователя с неверными данными
Изменение данных пользователя:
test_change_email - тест успешного изменения почты авторизованного пользователя
test_change_name - тест успешного изменения имени авторизованного пользователя
test_change_password - тест успешного изменения пароля авторизованного пользователя
test_change_all_data - тест на успешное изменение всех данных авторизованного пользователя
test_inability_change_all_data_without_login - тест на неуспешное изменение данных авторизованного, но не залогиненного пользователя
test_cannot_change_email_if_used_by_other_user - тест на неуспешное изменение почты авторизованного пользователя, если такая почта уже есть у другого пользователя

Тесты для заказа.
Создание заказа:
test_create_order_with_ingredients_without_login - тест на успешное создание заказа с ингредиентами без авторизации
test_create_order_without_ingredients_without_login - тест на не успешное создание заказа без ингредиентом без авторизации
test_create_order_non_existent_ingredients_without_login - тест на не успешное создание заказа с несуществующим ID ингредиента без авторизации
test_create_order_with_ingredients_user_authorized - тест на успешное создание заказа с ингредиентами с авторизацией
test_create_order_without_ingredients_user_authorized - тест на не успешное создание заказа без ингредиентом c авторизацией
test_create_order_non_existent_ingredients_user_authorized - тест на не успешное создание заказа с несуществующим ID ингредиента c авторизацией
Получение заказов конкретного пользователя:
test_orders_login_user - тест на получение заказов авторизованного пользователя
test_orders_without_login_user - тест на получение заказов не авторизованного пользователя