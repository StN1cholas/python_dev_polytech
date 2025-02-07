Нашей группой реализован бот, который с вашего личного аккаунта в Whatsapp рассылает тесты людям из вашего списка контактов. Мы использовали библиотеку selenium, автоматизирующую действия в веб-браузере.

Для того чтобы использовать бот необходимо установить библиотеку selenium, а также скачать ChromeDriver, соответствующий вашей версии Chrome. Узнать версию можно по этой ссылке: chrome://settings/help (вставьте в адресную строку), а скачать ChromeDriver по этой: https://developer.chrome.com/docs/chromedriver/downloads?hl=ru. Скачанный драйвер необходимо поместить в папку проекта.

# Описание процесса работы бота
После того как вы запустите код, вам нужно будет выполнить 2 действия: 
1. Отсканировать QR-код из мобильного приложения Whatsapp. Для этого в настройках приложения найдите раздел "Связанные устройства", войдите в него и нажмите "Связывание устройства". Это необходимо чтобы войти в ваш Whatsapp аккаунт в браузере.
2. В консоли введите имя контакта, которому хотите отправить тест. Имя должно быть введено идентично тому, как этот человек записан у вас в Whatsapp. Если необходимо, то можно писать по номеру 89218570167. Для того чтобы согласовать время проверки и действия необходимые с моей стороны, пожалуйста, напишите в телеграмм: @s3sh3 (Николаев Александр).

 Уточнение 1: для корректной работы в вашем чате с человеком уже должно быть хотя бы 1 сообщение.
 Уточнение 2: если вы сначала выполните действие (2), то у вас будет только 20 секунд чтобы отсканировать QR-код. Иначе программу придётся запускать заново.

После этого бот начнёт свою работу. Выбранному контакту будет отправлен тест из 4 вопросов с четырьмя вариантами ответа. Тестироемому нужно будет ввести цифру от 1 до 4, соответствующую выбранному варианту. Если ответ будет дан в другом формате или не дан вовсе, то будет считаться, что у пользователя нет ответа на поставленный вопрос (неправильный ответ).

После каждого ответа пользователю сообщается о его правильности\неправильности, а также показывается верный вариант при неправильном ответе. После прохождения всех четырёх вопросов выводится итоговый результат. Через 100 секунд после этого бот завершает работу (для удобства отладки и проверки).
