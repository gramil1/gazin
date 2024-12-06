import telebot,os
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))


# Пример вопросов для теста на IQ
questions = [
    {"question": "Сколько будет 2 + 2?", "answer" : "4"},
    {"question": "Сколько будет 5 * 5?", "answer" : "25"},
    {"question": "Сколько будет 10 * 5?", "answer" : "50"},
    {"question": "Сколько будет 2345667 + 234656789765?", "answer" : "234659135432"}
]

# Отслеживаем состояние прохождения теста
user_data = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для теста на IQ. Напиши /begin, чтобы начать тест.")

@bot.message_handler(commands=['begin'])
def start_test(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'current_question': 0, 'score': 0}
    send_next_question(chat_id)

def send_next_question(chat_id):
    user = user_data.get(chat_id)
    if user and user['current_question'] < len(questions):
        question = questions[user['current_question']]['question']
        bot.send_message(chat_id, question)
    else:
        bot.send_message(chat_id, f"Тест завершён! Ваш результат: {user['score']} из {len(questions)}")
        user_data.pop(chat_id, None)

@bot.message_handler(func=lambda message: True)
def check_answer(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        bot.send_message(chat_id, "Напиши /begin, чтобы начать тест на IQ.")
        return

    user = user_data[chat_id]
    current_q = questions[user['current_question']]
    if message.text == current_q['answer']:
        user['score'] += 1
        bot.send_message(chat_id, "Верно!")
    else:
        bot.send_message(chat_id, f"Неверно. Правильный ответ: {current_q['answer']}")

    user['current_question'] += 1
    send_next_question(chat_id)

bot.polling(non_stop=True)