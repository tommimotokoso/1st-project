import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('C:\ProgramData\chromedriver.exe')
#  pytest.driver.implicitly_wait(10)
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends1.herokuapp.com/login')

   yield

   pytest.driver.quit()


def test_show_all_my_pets():
   # Вводим email
   pytest.driver.find_element_by_id('email').send_keys('email')
   # Вводим пароль
   pytest.driver.find_element_by_id('pass').send_keys('password')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
   # Нажимаем кнопку для выпадающего меню "все питомцы/мои питомцы"
   pytest.driver.find_element_by_css_selector('button.navbar-toggler').click()
   # Выбираем "мои питомцы"
   ## Реализация явного ожидания (очень проблемное место, без ожидания, часто, здесь, тесты падали)
   button_my_pets = WebDriverWait(pytest.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, "//li/a"), 'Мои питомцы'))
   pytest.driver.find_element_by_link_text('Мои питомцы').click()
   # Находим число питомцев (надписью)
   ## Реализация явного ожидания (с учетом статистики пользователя для первого теста)
   table_of_my_pets_plus = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, "body/div[1]")))
   number_of_pets = pytest.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]').text.split()
   number_of_pets = int(number_of_pets[3])
   # Находим число питомцев на странице (карточки)
   pets = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]//tbody/tr')
   card_of_pets = len(pets)
   # Если числа питомцев совпадают - тест пройден
   assert number_of_pets == card_of_pets


def test_half_pets_with_photo():
   # Вводим email
   pytest.driver.find_element_by_id('email').send_keys('email')
   # Вводим пароль
   pytest.driver.find_element_by_id('pass').send_keys('password')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
   # Нажимаем кнопку для выпадающего меню "все питомцы/мои питомцы"
   pytest.driver.find_element_by_css_selector('button.navbar-toggler').click()
   # Выбираем "мои питомцы"
   ## Реализация явного ожидания (очень проблемное место; без ожидания, часто, здесь, тесты падали)
   button_my_pets = WebDriverWait(pytest.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, "//li/a"), 'Мои питомцы'))
   pytest.driver.find_element_by_link_text('Мои питомцы').click()
   # Находим число питомцев на странице (карточки)
   ## Реализация неявного ожидания элементов таблицы питомцев пользователя (фото, имя, порода, возраст)
   pytest.driver.implicitly_wait(10)
   pytest.driver.find_element_by_xpath('//th/img')
   pytest.driver.find_element_by_xpath('//tr/td')
   pets = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]//tbody/tr')
   card_of_pets = len(pets)
   images = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]//img')
   result = 0
   # Если картинка с пустым атрибутом "src", то добавляет счетчик на "+1"
   for i in range(len(images)):
      if images[i].get_attribute('src') == '':
         result = result + 1
   # Если счетчик питомцев с "пустыми картинками" меньше общего числа питомцев / 2 - тест пройден
   assert result < card_of_pets / 2

def test_full_descriptions():
   # Вводим email
   pytest.driver.find_element_by_id('email').send_keys('email')
   # Вводим пароль
   pytest.driver.find_element_by_id('pass').send_keys('password')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
   # Нажимаем кнопку для выпадающего меню "все питомцы/мои питомцы"
   pytest.driver.find_element_by_css_selector('button.navbar-toggler').click()
   # Выбираем "мои питомцы"
   ## Реализация явного ожидания (очень проблемное место, без ожидания, часто, здесь, тесты падали)
   button_my_pets = WebDriverWait(pytest.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, "//li/a"), 'Мои питомцы'))
   pytest.driver.find_element_by_link_text('Мои питомцы').click()
   ## Реализация явного ожидания (таблица пользователя)
   table_of_my_pets = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "all_my_pets")))
   descriptions = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]//td')
   for i in range(len(descriptions)):
   #Если в списке отсутсвуют пустые значения - тест пройден
      assert descriptions[i].text != ""

def test_different_names():
   # Вводим email
   pytest.driver.find_element_by_id('email').send_keys('email')
   # Вводим пароль
   pytest.driver.find_element_by_id('pass').send_keys('password')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
   # Нажимаем кнопку для выпадающего меню "все питомцы/мои питомцы"
   pytest.driver.find_element_by_css_selector('button.navbar-toggler').click()
   # Выбираем "мои питомцы"
   ## Реализация явного ожидания (очень проблемное место, без ожидания, часто, здесь, тесты падали)
   button_my_pets = WebDriverWait(pytest.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, "//li/a"), 'Мои питомцы'))
   pytest.driver.find_element_by_link_text('Мои питомцы').click()
   ## Реализация неявного ожидания элементов таблицы питомцев пользователя (фото, имя, порода, возраст)
   pytest.driver.implicitly_wait(10)
   pytest.driver.find_element_by_xpath('//th/img')
   pytest.driver.find_element_by_xpath('//tr/td')
   names = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]//td[1]')
   name_true = []
   for i in names:
      name_true.append(i.text)
   # Если в списке все имена уникальны - тест пройден
   assert len(list(name_true)) == len(set(name_true))

def test_duplicate_pets():
   # Вводим email
   pytest.driver.find_element_by_id('email').send_keys('email')
   # Вводим пароль
   pytest.driver.find_element_by_id('pass').send_keys('password')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
   # Нажимаем кнопку для выпадающего меню "все питомцы/мои питомцы"
   pytest.driver.find_element_by_css_selector('button.navbar-toggler').click()
   # Выбираем "мои питомцы"
   ## Реализация явного ожидания (очень проблемное место, без ожидания, часто, здесь, тесты падали)
   button_my_pets = WebDriverWait(pytest.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, "//li/a"), 'Мои питомцы'))
   pytest.driver.find_element_by_link_text('Мои питомцы').click()
   ## Реализация явного ожидания (таблица пользователя)
   table_of_my_pets = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "all_my_pets")))
   pets = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]//tr')
   pets_true = []
   for i in pets:
      pets_true.append(i.text)
   # Удаляем первую запись в полученном списке ("фото", "имя", "порода", "возраст")
   pets_true.pop(0)
   # Если в списке уникальны имя & порода & возраст (обязательно все вместе) - тест пройден
   assert len(list(pets_true)) == len(set(pets_true))

   pytest.driver.save_screenshot('result.png')
