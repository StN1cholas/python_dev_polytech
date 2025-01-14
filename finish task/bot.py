import json
import random
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime
import time


# Укажите путь к вашему chromedriver
service = Service(r'C:\Users\Nicholas\AppData\Local\chromedriver-win64\chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get('https://web.whatsapp.com')

# Имя контакта, которому будут отправляться вопросы
contact_name = input('Введите имя пользователя, который будет проходить тест: ')

print("Пожалуйста, отсканируйте QR-код")
time.sleep(20)


# Функция для отправки сообщения
def send_message(contact_name, message):
    time.sleep(2)
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.click()
    search_box.send_keys(contact_name)
    time.sleep(2)

    contact = driver.find_element(By.XPATH, f'//span[@title="{contact_name}"]')
    contact.click()

    message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true" and @data-tab="10"]')
    message_box.send_keys(message)
    message_box.send_keys('\n')


# Функция для получения последнего сообщения от пользователя
def get_last_message():
    time.sleep(15)  # Даем время на обновление чата
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


# Функция для загрузки тестов из JSON файла
def load_tests(file_path="tests.json"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден.")
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


# Функции для работы с answers.json
def load_answers(file_path="answers.json"):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_answers(answers, file_path="answers.json"):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(answers, file, ensure_ascii=False, indent=4)

def record_answer(contact_name, test_name, question, user_answer, correct, is_correct, file_path="answers.json"):
    answers = load_answers(file_path)
    if contact_name not in answers:
        answers[contact_name] = {}
    if test_name not in answers[contact_name]:
        answers[contact_name][test_name] = {"attempts": []}

    attempt_index = len(answers[contact_name][test_name]["attempts"])
    if len(answers[contact_name][test_name]["attempts"]) <= attempt_index:
        answers[contact_name][test_name]["attempts"].append({"questions": [], "score": 0})

    answers[contact_name][test_name]["attempts"][-1]["questions"].append({
        "question": question,
        "user_answer": user_answer,
        "correct": correct,
        "is_correct": is_correct
    })

    if is_correct:
        answers[contact_name][test_name]["attempts"][-1]["score"] += 1

    save_answers(answers, file_path)


# Загрузка тестов
try:
    tests = load_tests("tests.json")
    selected_test = random.choice(tests)

    # Отправляем тест
    send_message(contact_name, f"Тест: {selected_test['test_name']}")
    time.sleep(2)

    for index, q in enumerate(selected_test["questions"]):
        send_message(contact_name, f"Вопрос {index + 1}: {q['question']}")
        time.sleep(1)

        options_text = "\n".join(q["options"])
        send_message(contact_name, f"Выберите вариант ответа:\n{options_text}")
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
            else:
                print(f"Получен ответ: {user_answer}")
                break
            time.sleep(3)

        # Проверяем правильность ответа
        is_correct = user_answer == q["correct"]
        record_answer(
            contact_name=contact_name,
            test_name=selected_test["test_name"],
            question=q["question"],
            user_answer=user_answer,
            correct=q["correct"],
            is_correct=is_correct
        )

        if is_correct:
            send_message(contact_name, "Правильный ответ!")
        else:
            send_message(contact_name, f"Неправильный ответ. Правильный ответ: {q['correct']}")

        time.sleep(2)

    # Сохраняем итоговую статистику
    answers = load_answers()
    score = answers[contact_name][selected_test["test_name"]]["attempts"][-1]["score"]
    total_questions = len(selected_test["questions"])
    send_message(contact_name, f"Тест завершён. Верные ответы: {score}/{total_questions}")

except FileNotFoundError as e:
    print(e)
except Exception as e:
    print(f"Произошла ошибка: {e}")

# Завершаем работу
time.sleep(100)
driver.quit()
