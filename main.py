import sqlite3
import telebot
from gevent.libev.corecext import callback
from pyexpat.errors import messages
from telebot import types


db_name = "data/demo.db"

bot = telebot.TeleBot("7826590907:AAF3e4KsK8c3rUHHWSpjYvihuGdD8IhAzBs", parse_mode="HTML")


def get_question(level):
    global  q
    cn = sqlite3.connect(db_name)

    sql = '''SELECT * FROM Questions WHERE level = ? ORDER by random() LIMIT 1'''
    cur = cn.cursor()
    cur.execute(sql, [level])
    q = cur.fetchone()

    cn.commit()
    cn.close()
    return q


@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Привет, new - новая игра, rules - правила игры")


@bot.message_handler(commands= ["rules", "r"])
def game_rules(message):
    chat_id = message.chat.id
    with open(file= "data/rules.txt", encoding="utf-8") as rules_g:
        bot.send_message(chat_id, rules_g)


@bot.message_handler(commands=["new"])
def new_game(message):
    get_question(1)
    chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text=f"{q[2]}", callback_data= "1")
    button2 = types.InlineKeyboardButton(text=f"{q[3]}", callback_data= "2")
    button3 = types.InlineKeyboardButton(text=f"{q[4]}", callback_data= "3")
    button4 = types.InlineKeyboardButton(text=f"{q[5]}", callback_data= "4")
    keyboard.add(button1, button2)
    keyboard.add(button3, button4)
    bot.send_message(chat_id, f"Игра начинается. Вопрос: {q[1]}", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "1")
def next_turn(call):
    global q
    message = call.message
    chat_id = message.chat.id
    right_answer = q[7]
    if int(call.data) == int(right_answer):
        bot.send_message(chat_id, "Это правильный ответ. Следующий вопрос:")
    else:
        bot.send_message(chat_id, f"Это не верный ответ! Прощайте!")
    print(call.data)
    print(right_answer)
@bot.callback_query_handler(func=lambda call: call.data == "2")
def next_turn(call):
    message = call.message
    chat_id = message.chat.id
    right_answer = q[7]
    if int(call.data) == int(right_answer):
        bot.send_message(chat_id, "Это правильный ответ. Следующий вопрос:")
    else:
        bot.send_message(chat_id, f"Это не верный ответ! Прощайте!")
    print(call.data)
    print(right_answer)
@bot.callback_query_handler(func=lambda call: call.data == "3")
def next_turn(call):
    message = call.message
    chat_id = message.chat.id
    right_answer = q[7]
    if int(call.data) == int(right_answer):
        bot.send_message(chat_id, "Это правильный ответ. Следующий вопрос:")
    else:
        bot.send_message(chat_id, f"Это не верный ответ! Прощайте!")
    print(call.data)
    print(right_answer)

@bot.callback_query_handler(func=lambda call: call.data == "4")
def next_turn(call):
    message = call.message
    chat_id = message.chat.id
    right_answer = q[7]
    if int(call.data) == int(right_answer):
        bot.send_message(chat_id, "Это правильный ответ. Следующий вопрос:")
    else:
        bot.send_message(chat_id, f"Это не верный ответ! Прощайте!")
    print(call.data)
    print(right_answer)





bot.infinity_polling()

