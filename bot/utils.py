import datetime
import os
import re
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bot import settings
from selenium.webdriver.common.action_chains import ActionChains


def form_write(data: dict[str, str | int]) -> str:
    birthdate = data.get("birthdate")
    year, month, day = birthdate.split("-")  # type: ignore
    # создаем экземпляр браузера
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 5)

    # открываем страницу с формой
    driver.get(settings.FORM_URL)

    # Были проблемы с вводом из-за кириллицы, поэтому использую ActionChains
    # кликаем на поле ввода
    input_field = wait.until(EC.presence_of_element_located((By.NAME, "name")))
    ActionChains(driver).click(input_field).perform()
    # заполняем имя
    ActionChains(driver).send_keys(data.get("name")).perform()

    # переходим к фамилии
    input_field = wait.until(EC.presence_of_element_located((By.NAME, "lastname")))
    ActionChains(driver).click(input_field).perform()
    # заполняем фамилию
    ActionChains(driver).send_keys(data.get("last_name")).perform()

    # переходим к следующим полям
    next_button = driver.find_element(By.CLASS_NAME, "b24-form-btn")
    next_button.click()

    # заполняем e-mail и номер телефона
    email_element = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    email_element.send_keys(data.get("email"))
    driver.find_element(By.NAME, "phone").send_keys(data.get("phone"))
    # переходим к следующим полям
    next_button.click()

    # заполняем дату рождения
    birthdate_field = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'input[readonly][class="b24-form-control"]')
        )
    )
    # кликаем на поле, чтобы открыть календарь
    birthdate_field.click()
    # находим выпадающие меню
    dropdown_elems = driver.find_elements(By.CSS_SELECTOR, ".vdpPeriodControl select")
    # выберем месяц по значению атрибута value в option элементе
    select = Select(dropdown_elems[0])
    select.select_by_value(str(int(month) - 1))  # Выбираем месяц
    select = Select(dropdown_elems[1])
    select.select_by_value(year)  # Выбираем год

    # В data-id не используются ведущие нули для месяца и дня
    if int(month) < 10 or int(day) < 10:
        month = month[1] if int(month) < 10 else month
        day = day[1] if int(day) < 10 else day
        birthdate = "-".join((year, month, day))

    day_select = driver.find_element(
        By.CSS_SELECTOR,
        "td[data-id='{}']".format(birthdate),  # Выбираем день
    )
    day_select.click()

    # Отправляем форму
    send_button = driver.find_element(
        By.CSS_SELECTOR, 'button.b24-form-btn[type="submit"]'
    )
    send_button.click()

    # Ждем пока кнопка пропадет
    while send_button.get_attribute("background-color") == "#0f58d0":
        print(1)
    time.sleep(2)  # слип, чтобы страница прогрузилась
    # получаем текущую дату и время
    now = datetime.datetime.now()
    # форматируем дату и время в нужный формат
    timestamp = now.strftime("%Y-%m-%d_%H-%M")
    user_id = data.get("user_id")

    # заменяем ":", потому что иначе не читается файл
    filename = f"{timestamp}_{user_id}.png"
    file_path = os.path.join(settings.PATH_FOR_SCREENSHOTS, filename)
    driver.save_screenshot(file_path)

    # закрываем браузер
    driver.quit()

    return file_path


# Регулярки для e-mail, телефона, имени и фамилии
email_pattern = r"^[a-zA-Z0-9_.-]+@[a-zA-Z0-9]+\.[a-z]{2,3}$"
phone_pattern = r"^\+?\d{1,3}\s?(\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}$"
name_pattern = r"^[a-zA-Zа-яА-Я]+$"


email_regex = re.compile(email_pattern)
phone_regex = re.compile(phone_pattern)
name_regex = re.compile(name_pattern)
