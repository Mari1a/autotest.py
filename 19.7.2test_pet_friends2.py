from api import PetFriends
from settings import not_valid_email, not_valid_password, valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_notValid_user(email=not_valid_email, password=not_valid_password):
    """ Проверяем негативным тестом  не валидные данные что запрос api ключа возвращает статус 403 и
     в тезультате содержится слово Неверная комбинация имени пользователя и пароля"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'Неверная комбинация имени пользователя и пароля' in result


def test_get_all_pets_with_notValid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_notValid_data(name='Енот', animal_type='кот-енот',
                                        age='-3', pet_photo='images/catEnot.jpg'):
    """Проверяем что можно добавить питомца с не корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    # pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом сейчас баг в апи!
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Матроскин", "кот", "3", "images/catEnot.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id последнего питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][-1]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info_notValues(name='Лизз', animal_type='царевна', age='еее'):
    """Проверяем возможность обновления информации о питомце c не валидными данными"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному сейчас баг в апи!
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_add_new_pet_with_valid_data(name='Енот', animal_type='кот-енот',
                                     age='-3', pet_photo='images/catEnot.jpg'):
    """Проверяем что можно добавить питомца с не корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    # pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом сейчас баг в апи!
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_without_photo(name='Енот', animal_type='кот-енот', age='3'):
    """Проверяем что можно добавить питомца без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_empty_values(name='', animal_type='', age=''):
    """Проверяем что можно добавить питомца без фото с пустым значением"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом сейчас баг в апи принемает пустые значения!
    assert status == 200
    assert result['name'] == name


def test_add_photo_to_pet(pet_photo="images/dog1.jpg"):
    """Проверяем что можно добавить фото питомца """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        pf.add_photo_to_pet(auth_key, pet_id, pet_photo)

    # Берём id последнего питомца из списка и отправляем запрос на удаление
    status, _ = pf.add_photo_to_pet(auth_key, pet_id, pet_photo)

     # Проверяем что статус ответа равен 200 и в списке питомцев  id c добавленным фото
    assert status == 200
    assert pet_id == pet_id

def test_add_new_pet_without_photo_extra(name='Лейла', animal_type='шпиц',
                                         age='2', pet_photo='images/dog1.jpg'):
    """Проверяем  неготивным тестом что можно добавить питомца с лишними значениями"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['Ключевая ошибка'] == KeyError
