import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bot import settings
from bot.celery_config import app


@app.task
def form_write(data: dict[str, str]) -> str:
    birthdate = data.get("birthdate")
    year, month, _ = birthdate.split("-")  # type: ignore
    # создаем экземпляр браузера
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 5)

    # открываем страницу с формой
    driver.get("https://b24-iu5stq.bitrix24.site/backend_test/")

    # заполняем первые имя фамилию
    driver.find_element(By.NAME, "name").send_keys(data.get("name"))
    driver.find_element(By.NAME, "lastname").send_keys(data.get("last_name"))

    # # переходим к следующим полям
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
    day_select = driver.find_element(
        By.CSS_SELECTOR,
        "td[data-id='{}']".format(data.get("birthdate")),  # Выбираем день
    )
    day_select.click()

    # Отправляем форму
    send_button = driver.find_element(
        By.CSS_SELECTOR, 'button.b24-form-btn[type="submit"]'
    )
    send_button.click()

    # Ждем пока кнопка пропадет
    while send_button.get_attribute("background-color") == "#0f58d0":
        pass
    time.sleep(2)  # слип, чтобы страница прогрузилась
    # получаем текущую дату и время
    now = datetime.datetime.now()
    # форматируем дату и время в нужный формат
    timestamp = now.strftime("%Y-%m-%d_%H:%M")
    user_id = data.get("user_id")
    filename = f"{timestamp}_{user_id}.png"
    driver.save_screenshot(settings.PATH_FOR_SCREENSHOTS + f"{timestamp}_{user_id}.png")

    input("Нажмите Enter для выхода...")
    # закрываем браузер
    driver.quit()

    return filename