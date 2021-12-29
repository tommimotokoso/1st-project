from api import PetFriends
from settings import valid_email, valid_password, no_valid_email, no_valid_password, pet_id, token

pf = PetFriends()

#1 Get-запрос на получение Api-ключа
def test_get_api_key_success(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
    print(result)


#2 Get-запрос с невалидным email
def test_get_api_key_for_no_valid_email_failed(email=no_valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403


#3 Get-запрос без пароля
def test_get_api_key_for_no_valid_password_failed(email=valid_email, password=no_valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403


#4 Get-запрос с фильтром my_pets
def test_get_filter_with_valid_key_success(filter='my_pets'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0
    print(result)


#5  Get-запрос с несуществующим фильтром
def test_get_filter_with_valid_key_failed(filter='users'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status != 200


#6 Post-запрос на добавление питомца
def test_add_new_pet_success(name='вова', animal_type='русская борзая', age='60+', pet_photo='images/вова.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age


#7 Delete-запрос на удаление питомца
def test_delete_pet_success():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.delete_pet(auth_key, my_pets['pets'][0]['id'])
    assert status == 200
    assert pet_id not in my_pets.values()


#8 Post/Delete-запрос на создание и удаление питомца
def test_delete_self_pet_success():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
# Создаем нового питомца
    pf.add_new_pet_with_photo(auth_key, "тест", "тест", "5", "images/вова.jpg")
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    print(my_pets)
# удаляем нового питомца
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


#9 Post-запрос на создание питомца без фото
def test_new_pet_simple_success(name='володимир', animal_type='тсарь', age='60'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age


#10 Put-запрос на изменение имени, типа, и возраста питомца
def test_change_pet_success(name='nne', animal_type='nne', age='5'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.change_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

