Каждый хотя бы раз сталкивался с проблемой, когда тебе прислали голосовое сообщение. а возможности его прослушать нет. особенно остро вопрос стоит в Telegram. 
Да, в данной соцюсети существует возможность распознавания голосового сообщения, но данная взможность есть лишь у обладателей премиум подписки, которая в месяц стоит 329руб. 
Дороговато ради одних лишь голосовых сообщений, учитывая отсутствие культуры приобретения контента (если бы она была, не было бы огромного количества пиратских сайтов просмотра фильмов, сериалов и т.д.).
Чтобы все могли оставаться "в теме", даже когда не у каждого есть возможность прослушать их, мы решили научить бота переводить голосовые в текст.

Нейронных сетей, заточенных под распознавание голоса, свыше десятка, но они требуют серьёзных вычислительных мощностей, чего мой не самый мощный сервер не может предоставить.
Готовые сервисы тоже есть, но практически все - платные. Не беря в расчёт "пробные периоды" из бесплатных (вернее с бесплатным лимитом в месяц) есть два сервиса:

Google Cloud - думаю не стоит рассказывать о Google. Они предлагают бесплатный тариф - 60 минут в месяц.
SpeechFlow - сервис, позиционирующий себя как "лидера рынка". Поддерживают транскрипцию с 14-ти языков. Предлагают бесплатный тариф: 30 минут онлайн-распознавания (на сайте) и пять часов по API в месяц.
Сервис от Google нам не подходит: 60 минут на целый месяц слишком мало, поэтому выбор был сделан в пользу SpeechFlow. 

Регистрация и получение API-ключа.
Переходим на сайт сервиса: https://speechflow.io/ru/
После регистрации попадаем в личный кабинет. Там в левой панели выбираем раздел "API".
На открывшейся странице нажимаем кнопку "Сгенерировать ключ API".
В появившемся окне будет две строки:
KeyId - идентификатор ключа
KeySecret - секретный ключ
