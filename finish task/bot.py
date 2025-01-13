from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime
import time


# Укажите путь к вашему chromedriver
service = Service(r'C:\Users\1\Desktop\chromedriver-win64\chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get('https://web.whatsapp.com')

# Имя контакта, которому будут отправляться вопросы
contact_name = 'Алина Зайчик'


print("Пожалуйста, отсканируйте QR-код")
time.sleep(30)


# Функция для отправки сообщения
def send_message(contact_name, message):
    # Найдите контакт по имени
    time.sleep(2)
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.click()
    search_box.send_keys(contact_name)
    time.sleep(2)

    # Выберите контакт из результатов поиска
    contact = driver.find_element(By.XPATH, f'//span[@title="{contact_name}"]')
    contact.click()

    # Найдите поле ввода сообщения и отправьте сообщение
    message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true" and @data-tab="10"]')
    message_box.send_keys(message)
    message_box.send_keys('\n')  # Отправка сообщения


# Функция для получения последнего сообщения от пользователя
def get_last_message():
    time.sleep(30)  # Даем время на обновление чата
    messages = driver.find_elements(By.XPATH,'//div[contains(@class, "message-in")]//span[contains(@class, "selectable-text")]/span')

    if messages:
        last_message_element = messages[-1]
        last_message = last_message_element.text  # Получаем текст последнего сообщения

        time_xpath = '(//div[contains(@class, "message-in")]//span[@class="x1rg5ohu x16dsc37" and @dir="auto"])[last()]'
        time_element = driver.find_element(By.XPATH, time_xpath)
        time_text = time_element.text

        # Преобразуем время ответа в datetime
        last_message_time = datetime.strptime(time_text,'%H:%M')


        # Проверяем, является ли последнее сообщение цифрой от 1 до 4
        if last_message.isdigit() and 1 <= int(last_message) <= 4:
            # Проверяем, что время ответа больше или равно времени вопроса
            if last_message_time >= last_message_time_out:
                return last_message  # Возвращаем текст последнего сообщения, если оно в диапазоне и время корректно
            else:
                return "None"
        else:
            return "None"  # Если сообщение не в диапазоне, возвращаем None
    else:
        return "None " # Если нет сообщений, возвращаем None


# Пример вопросов и ответов
questions = [
    {
        "question": "Какой язык программирования используется для веб-разработки?",
        "options": ["1. Python", "2. JavaScript", "3. Java", "4. C#"],
        "correct": "2"
    },
    {
        "question": "Какой фреймворк используется для разработки на Python?",
        "options": ["1. Django", "2. React", "3. Angular", "4. Vue"],
        "correct": "1"
    }
]

# Проход по вопросам
for q in questions:
    send_message(contact_name, q["question"])
    time.sleep(1)

    # Формируем текст с вариантами ответов и отправляем его
    options_text = " ".join(q["options"])
    send_message(contact_name, f"Выберите вариант ответа: {options_text}")
    time_xpath_out = '(//div[contains(@class, "message-out")]//span[@class="x1rg5ohu x16dsc37" and @dir="auto"])[last()]'
    time_element_out = driver.find_element(By.XPATH, time_xpath_out)
    time_text_out = time_element_out.text
    last_message_time_out = datetime.strptime(time_text_out, '%H:%M')
    time.sleep(10)

    # Ждем ответа пользователя
    print("Ожидание ответа...")

    # Ожидание и проверка ответа
    user_answer = "None"
    for _ in range(20):  # Проверяем в течение 10 секунд
        user_answer = get_last_message()

        if user_answer == "None":
            print("Ответ не получен за отведенное время.")

        if user_answer:
            print(f"Получен ответ: {user_answer}")
            break
        time.sleep(1)

    # Проверка правильности ответа
    if user_answer:
        correct_option = q["correct"]
        if user_answer.startswith(correct_option):
            print("Правильный ответ!")
            send_message(contact_name, 'Правильный ответ!')
        else:
            print("Неправильный ответ.")
            send_message(contact_name, f"Неправильный ответ. Правильный ответ - {correct_option}")
        time.sleep(30)
    else:
        print("Ответ не получен.")
        time.sleep(30)

# Закрытие драйвера после завершения


time.sleep(100)
driver.quit()



