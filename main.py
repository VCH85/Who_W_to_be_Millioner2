import telebot
from telebot import types
import sqlite3
import random
import datetime

# Токен вашего бота
TOKEN = '7826590907:AAF3e4KsK8c3rUHHWSpjYvihuGdD8IhAzBs'

# Подключение к базе данных
conn = sqlite3.connect('data/questions.db', check_same_thread=False)
cursor = conn.cursor()

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения состояния пользователей
users_state = {}

# Стоимость вопросов
PRIZES = [3000000, 1500000, 800000, 400000, 200000, 100000, 50000, 25000, 15000, 10000, 5000, 3000, 2000, 1000, 500]

# Несгораемые суммы
SAFETY_NETS = [5000, 10000, 50000, 100000, 200000, 400000, 800000, 1500000, 3000000]

# Список подсказок
HINTS = ['Помощь зала', '50 на 50', 'Звонок другу', 'Право на ошибку', 'Замена вопроса']


# Функция для получения случайного вопроса определенного уровня
def get_random_question(level):
    cursor.execute("SELECT * FROM questions WHERE level = ?", (level,))
    rows = cursor.fetchall()
    return random.choice(rows) if rows else None


# Функция для обработки начала игры
@bot.message_handler(commands=['start'])
def start_game(message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name

    users_state[chat_id] = {
        "current_level": 1,
        "total_score": 0,
        "used_hints": [],
        "safety_net": SAFETY_NETS[0],
        "game_over": False
    }

    bot.send_message(chat_id, f"Здравствуйте, {user_name}! Добро пожаловать в игру 'Кто хочет стать миллионером?'")
    ask_next_question(chat_id)


# Функция для вывода следующего вопроса
def ask_next_question(chat_id):
    state = users_state.get(chat_id)
    if not state or state["game_over"]:
        return

    current_level = state["current_level"]
    question_data = get_random_question(current_level)

    if not question_data:
        bot.send_message(chat_id, "Извините, но у нас нет больше вопросов этого уровня.")
        return

    question_text = question_data[1]
    options = [question_data[2], question_data[3], question_data[4],
               question_data[5]]
    correct_answer = question_data[6] - 1

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for i in range(4):
        button = types.InlineKeyboardButton(text=f"{chr(ord('A') + i)}. {options[i]}", callback_data=str(i))
        keyboard.add(button)

    bot.send_message(chat_id, f"Вопрос №{current_level}: {question_text}", reply_markup=keyboard)


# Обработчик нажатия кнопок вариантов ответа
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    state = users_state.get(chat_id)
    if not state or state["game_over"]:
        return

    answer_index = int(call.data)
    question_data = get_random_question(state["current_level"])
    correct_answer = int(question_data[7])
    print(question_data[7],correct_answer)
    if answer_index == correct_answer:
        prize = PRIZES[state["current_level"] - 1]
        state["total_score"] = prize

        next_level = state["current_level"] + 1
        if next_level > len(PRIZES):
            end_game(chat_id, prize)
        else:
            state["current_level"] = next_level
            bot.edit_message_text(f"Правильный ответ! Вы выиграли {prize}. Переходим к следующему вопросу.", chat_id,
                                  call.message.message_id)
            ask_next_question(chat_id)
    else:
        safety_net = state["safety_net"]
        end_game(chat_id, safety_net)


# Завершение игры
def end_game(chat_id, final_score):
    state = users_state.get(chat_id)
    if not state:
        return

    state["game_over"] = True
    bot.send_message(chat_id,
                     f"К сожалению, вы дали неверный ответ. Ваша итоговая сумма составляет {final_score}. Спасибо за участие!")

    # Сохранение результата в базу данных
    username = bot.get_chat_member(chat_id, chat_id).user.first_name
    cursor.execute("INSERT INTO records (username, score, timestamp) VALUES (?, ?, ?)",
                   (username, final_score, datetime.datetime.now()))
    conn.commit()


# Команда для просмотра топ-10 игроков
@bot.message_handler(commands=['top'])
def show_top_records(message):
    chat_id = message.chat.id

    cursor.execute("SELECT username, score FROM records ORDER BY score DESC LIMIT 10")
    rows = cursor.fetchall()

    top_text = "Топ-10 игроков:\n"
    for i, row in enumerate(rows):
        username, score = row
        top_text += f"{i + 1}. {username} - {score}\n"

    bot.send_message(chat_id, top_text)


# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)